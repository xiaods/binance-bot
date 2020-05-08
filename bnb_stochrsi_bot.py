# coding: utf-8
"""
    StochasticRSI 策略， K线 < 20，买入，> 80 卖出。  D线是K平滑均值线，辅助提供当前盘是涨还是跌的趋势
    当K > D， 涨势， D > K ， 跌势
"""
import pandas as pd
import talib
import numpy as np #computing multidimensionla arrays

import time
from datetime import datetime
import sys
import signal

import logging
from logging.handlers import TimedRotatingFileHandler
import re

# Initialize Client and connect to Binance
from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor

from settings import MarginAccount

from settings import BinanceKey1
api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']
client = Client(api_key, api_secret, {"verify": True, "timeout": 10000})


# logger初始化
#################################### Logging #################################################
logger = logging.getLogger("BinanceBot")

log_format = "%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(filename)s[line:%(lineno)d] %(message)s"
log_level = 10
handler = TimedRotatingFileHandler("binancebot.log", when="midnight", interval=1)
handler.setLevel(log_level)
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
handler.suffix = "%Y%m%d"
handler.extMatch = re.compile(r"^\d{8}$") 
logger.addHandler(handler)
logger.setLevel(logging.INFO)
##############################################################################################

# step0 初始化参数，请咨询核对调优
symbol = MarginAccount['pair_symbol']  #<---交易对
eos_symbol = MarginAccount['eos_symbol']
usdt_symbol = MarginAccount['usdt_symbol']
loan = MarginAccount['loan']
depth = MarginAccount['depth']
qty = loan / depth
# 最大交易对
max_margins = (depth * 2) * float(0.6)
# 账户币余额必须大于30%才能交易
free_coin_limit_percentile = float(0.3)

# BinanceSocketManager 全局变量初始化
bm = None
conn_key = None
indicator = None

def run():
    initialize_arb()

def initialize_arb():
    welcome_message = "\n\n---------------------------------------------------------\n\n"
    welcome_message+= "Binance auto trading bot\n"
    bot_start_time = str(datetime.now())
    welcome_message+= "\nBot Start Time: {}\n\n\n".format(bot_start_time)
    logger.info(welcome_message)
    time.sleep(1)
    status = client.get_system_status()
    logger.info("\nExchange Status: {}" % status)

    # step1 创建对手单,第一入口
    # 1.2 借出币
    loan_asset(eos_symbol,loan)
    # 监听Stoch RSI指标发动指标
    stochrsi_order(symbol,qty)

    # step2 监听杠杆交易
    global bm, conn_key
    bm = BinanceSocketManager(client)
    conn_key = bm.start_margin_socket(process_message)
    logger.info("websocket Conn key: {}".format(conn_key) )
    bm.start()

    # 30分钟ping user websocket，key可以存活1个小时
    while True:
        get_margin_stream_keepalive(conn_key)
        time.sleep(60 * 30)


def stochrsi_order(symbol, qty):
    # Main program
    while True:
        # Get Binance Data into dataframe
        candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE)
        df = pd.DataFrame(candles)
        df.columns=['timestart','open','high','low','close','?','timeend','?','?','?','?','?']
        df.timestart = [datetime.fromtimestamp(i/1000) for i in df.timestart.values]
        df.timeend = [datetime.fromtimestamp(i/1000) for i in df.timeend.values]

        # Compute RSI after fixing data
        float_data = [float(x) for x in df.close.values]
        np_float_data = np.array(float_data)
        rsi = talib.RSI(np_float_data, 14)
        df['rsi'] = rsi

        # Compute StochRSI using RSI values in Stochastic function
        mystochrsi = Stoch(df.rsi, df.rsi, df.rsi, 3, 3, 14)
        df['MyStochrsiK'],df['MyStochrsiD'] = mystochrsi

        time.sleep(1) # Sleep for 1 second. So IP is not rate limited. Can be faster. Up to 1200 requests per minute.


        newestcandlestart = df.timestart.astype(str).iloc[-1] #gets last time
        newestcandleend = df.timeend.astype(str).iloc[-1] #gets current time?
        newestcandleclose = df.close.iloc[-1] #gets last close
        newestcandleRSI = df.rsi.astype(str).iloc[-1] #gets last rsi
        newestcandleK = df.MyStochrsiK.astype(str).iloc[-1] #gets last rsi
        newestcandleD = df.MyStochrsiD.astype(str).iloc[-1] #gets last rsi

        """
        当%K线和%D线相交时，也会产生买入和卖出信号：
        当%K线在%D线上方交叉时，产生买入信号，当%K线在%D线下方交叉时，产生卖出信号。
        但是，由于频繁的交叉，可能会产生错误的信号。
        """
        global indicator
        if float(newestcandleD) <= float(20) and float(newestcandleK) > float(newestcandleD):
            logger.info("LONG: K:{}> D:{}".format(newestcandleK, newestcandleD))
            indicator = "LONG"
            new_margin_order(symbol,qty)  #做多
        if float(newestcandleD) >= float(80) and float(newestcandleK) < float(newestcandleD):
            logger.info("SHORT: K:{} < D:{}".format(newestcandleK, newestcandleD))
            indicator = "SHORT"
            new_margin_order(symbol,qty)  #做空

def process_message(msg):
    if msg['e'] == 'error':
        error_msg = "\n\n---------------------------------------------------------\n\n"
        error_msg += "websocket error:\n"
        error_msg += msg.get('m')
        logger.warning(error_msg)
        # close and restart the socket
        global conn_key
        bm.stop_socket(conn_key)
        conn_key = bm.start_margin_socket(process_message)
        logger.info("renewer websocket Conn key: {}".format(conn_key))
    else:
        # process message normally
        # 单边出现，等待交易员操作，保持当前挂单
        if is_max_margins(max_margins) == True:
            logger.warning("Come across max margins limits....return, don't do order anymore.")
            return

        # 处理event executionReport
        if msg.get('e') == 'executionReport' and msg.get('s')  == symbol:
            logger.info(msg)
        # 当有交易成功的挂单，挂起新的网格对手单
        if msg.get('e') == 'executionReport' and msg.get('s')  == symbol and msg.get('X') == ORDER_STATUS_FILLED:
            new_margin_order(symbol,qty)

def new_margin_order(symbol,qty):
    # 当前报价口的买卖价格
    ticker = client.get_orderbook_ticker(symbol=symbol)
    logger.info("Current bid price: {}".format(ticker.get('bidPrice')))
    logger.info("Current ask price: {}".format(ticker.get('askPrice')))

    #计算当前账号的币的余额够不够，账户币余额必须大于30%才能交易
    account = client.get_margin_account()
    userAssets = account.get('userAssets')
    free_coin = float(0)
    for asset in userAssets:
        if asset.get('asset') == eos_symbol:
            free_coin = float(asset.get('free'))
    # 规则：账户币余额必须大于 free_coin_limit_percentile 才能交易
    if free_coin < loan * free_coin_limit_percentile:
        logger.warning("Current Account coin balance is less then 30%. don't do order anymore.")
        return

    # LONG or SHORT
    if indicator == "LONG":
        buy_price = float(ticker.get('bidPrice'))*float(1)
        buy_price = '%.4f' % buy_price

        sell_price = float(ticker.get('askPrice'))*float(1+0.2)
        sell_price = '%.4f' % sell_price

        buy_order = client.create_margin_order(symbol=symbol,
                                       side=SIDE_BUY,
                                       type=ORDER_TYPE_LIMIT,
                                       quantity=qty,
                                       price=buy_price,
                                       timeInForce=TIME_IN_FORCE_GTC)

        sell_order = client.create_margin_order(symbol=symbol,
                                       side=SIDE_SELL,
                                       type=ORDER_TYPE_LIMIT,
                                       quantity=qty,
                                       price=sell_price,
                                       timeInForce=TIME_IN_FORCE_GTC)
    elif indicator == "SHORT":
        buy_price = float(ticker.get('bidPrice'))*float(1-0.2)
        buy_price = '%.4f' % buy_price

        sell_price = float(ticker.get('askPrice'))*float(1)
        sell_price = '%.4f' % sell_price

        buy_order = client.create_margin_order(symbol=symbol,
                                       side=SIDE_BUY,
                                       type=ORDER_TYPE_LIMIT,
                                       quantity=qty,
                                       price=buy_price,
                                       timeInForce=TIME_IN_FORCE_GTC)

        sell_order = client.create_margin_order(symbol=symbol,
                                       side=SIDE_SELL,
                                       type=ORDER_TYPE_LIMIT,
                                       quantity=qty,
                                       price=sell_price,
                                       timeInForce=TIME_IN_FORCE_GTC)

    else:
        print("NO CHANCE: indicator:{}".format(indicator))

'''
purpose: 杠杆交易怕平仓，所以通过最简化的交易单数可以判断出是否超出仓位

'''
def is_max_margins(max_margins):
    orders = client.get_open_margin_orders(symbol=symbol)
    if len(orders) > max_margins:
        return True
    else:
        return False

'''
purpose: 自动借币

if account.loan 有币:
    pass
'''
def loan_asset(eos_symbol, qty):
    account = client.get_margin_account()
    userAssets = account.get('userAssets')
    origin_loan = float(0)
    for asset in userAssets:
        if asset.get('asset') == eos_symbol:
            origin_loan = float(asset.get('borrowed'))
    qty = qty - origin_loan
    if qty <= float(0):
        logger.info('don\'t need loan, original loan: {}'.format(origin_loan))
        pass
    else:
        transaction = client.create_margin_loan(asset=eos_symbol,
                                            amount=qty)
        logger.info(transaction)

# StochasticRSI Function
def Stoch(close,high,low, smoothk, smoothd, n):
    lowestlow = pd.Series.rolling(low,window=n,center=False).min()
    highesthigh = pd.Series.rolling(high, window=n, center=False).max()
    K = pd.Series.rolling(100*((close-lowestlow)/(highesthigh-lowestlow)), window=smoothk).mean()
    D = pd.Series.rolling(K, window=smoothd).mean()
    return K, D

'''
Purpose: Keepalive a user data stream to prevent a time out.
User data streams will close after 60 minutes.
It's recommended to send a ping about every 30 minutes.
'''
def get_margin_stream_keepalive(listen_key):
    result = client.margin_stream_keepalive(listen_key)
    return result


def term_sig_handler(signum, frame):
    print('catched singal: %d' % signum)
    reactor.stop()
    sys.exit()

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, term_sig_handler)
    signal.signal(signal.SIGINT, term_sig_handler)
    signal.signal(signal.SIGHUP, term_sig_handler)
    run()