# coding: utf-8
"""
    StochasticRSI 策略， K线 < 20，卖出，> 80 买入。  D线是K平滑均值线，辅助提供当前盘是涨还是跌的趋势
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
pair_symbol = MarginAccount['pair_symbol']  #<---交易对
coin_symbol = MarginAccount['coin_symbol']
usdt_symbol = MarginAccount['usdt_symbol']
loan = MarginAccount['loan']
depth = MarginAccount['depth']
qty = loan / depth
base_balance = MarginAccount['base_balance']
# 最大交易对
max_margins = MarginAccount['max_margins']
# 账户币余额必须大于30%才能交易
free_coin_limit_percentile = MarginAccount['free_coin_limit_percentile']
# 账户余额必须大于30%才能交易
free_cash_limit_percentile = MarginAccount['free_cash_limit_percentile']
# 价格精度
price_accuracy = MarginAccount['price_accuracy']

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
    loan_asset(coin_symbol,loan)
    # 监听Stoch RSI指标发动指标
    stochrsi_order(pair_symbol,qty)

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
    # Get Binance Data into dataframe, when k x d get correct indicator
    candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE)
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
    if float(newestcandleK) <= float(20) and newestcandleK <= newestcandleD:
        logger.info("LONG: RSI:{} K:{} D:{}".format(newestcandleRSI,newestcandleK, newestcandleD))
        indicator = "LONG"  #做多
    elif float(newestcandleK) >= float(80) and newestcandleK >= newestcandleD:
        logger.info("SHORT: RSI:{} K:{} D:{}".format(newestcandleRSI,newestcandleK, newestcandleD))
        indicator = "SHORT" #做空
    else:
        logger.info("NORMAL: RSI:{} K:{} D:{}".format(newestcandleRSI,newestcandleK, newestcandleD))
        indicator = "NORMAL"   #正常网格
    
    #  下单
    new_margin_order(symbol,qty) 

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
        if msg.get('e') == 'executionReport' and msg.get('s')  == pair_symbol:
            logger.info(msg)
        # 当有交易成功的挂单，挂起新的RSI对手单
        if msg.get('e') == 'executionReport' and msg.get('s')  == pair_symbol and msg.get('X') == ORDER_STATUS_FILLED:
            stochrsi_order(pair_symbol,qty)

def new_margin_order(symbol,qty):
    # 当前报价口的买卖价格
    ticker = client.get_orderbook_ticker(symbol=symbol)
    logger.info("Current bid price: {}".format(ticker.get('bidPrice')))
    logger.info("Current ask price: {}".format(ticker.get('askPrice')))

    #计算当前账号的币的余额够不够，账户币余额必须大于30%才能交易
    account = client.get_margin_account()
    userAssets = account.get('userAssets')
    free_coin = float(0)
    free_cash = float(0)
    for asset in userAssets:
        if asset.get('asset') == coin_symbol:
            free_coin = float(asset.get('free'))
        if asset.get('asset') == usdt_symbol:
            free_cash = float(asset.get('free'))
    # 规则：账户币余额必须大于 free_coin_limit_percentile 才能交易
    if free_coin < loan * free_coin_limit_percentile:
        logger.warning("Current Account coin balance is less then {}%. don't do order anymore.".format(free_coin_limit_percentile * 100))
        repay_coin(pair_symbol, coin_symbol, loan * 0.5)
        return
    if free_cash < base_balance * free_cash_limit_percentile:
        logger.warning("Current Account cash balance is less then {}%. don't do order anymore.".format(free_cash_limit_percentile * 100))
        return

    # LONG or SHORT
    if indicator == "LONG":
        buy_price = float(ticker.get('bidPrice'))*float(1)
        buy_price = price_accuracy % buy_price

        buy_order = client.create_margin_order(symbol=symbol,
                                       side=SIDE_BUY,
                                       type=ORDER_TYPE_LIMIT,
                                       quantity=qty,
                                       price=buy_price,
                                       timeInForce=TIME_IN_FORCE_GTC)

        logger.info("做多：买单ID:{}, 价格：{}， 数量：{}".format(buy_order, buy_price, qty))

    elif indicator == "SHORT":
        sell_price = float(ticker.get('askPrice'))*float(1)
        sell_price = price_accuracy % sell_price

        sell_order = client.create_margin_order(symbol=symbol,
                                       side=SIDE_SELL,
                                       type=ORDER_TYPE_LIMIT,
                                       quantity=qty,
                                       price=sell_price,
                                       timeInForce=TIME_IN_FORCE_GTC)

        logger.info("做空：卖单ID:{}, 价格：{}， 数量：{}".format(sell_order, sell_price, qty)) 

    elif indicator == "NORMAL":
        buy_price = float(ticker.get('bidPrice'))*float(1-0.005)
        buy_price = price_accuracy % buy_price

        sell_price = float(ticker.get('askPrice'))*float(1+0.005)
        sell_price = price_accuracy % sell_price

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
        logger.info("常单：买单ID:{}, 价格：{}， 数量：{}".format(buy_order, buy_price, qty))
        logger.info("常单：卖单ID:{}, 价格：{}， 数量：{}".format(sell_order, sell_price, qty)) 
    else:
        print("NO CHANCE: indicator:{}".format(indicator))


'''
purpose: coin补仓, 提供50%的币的数量
'''
def repay_coin(pair_symbol, coin_symbol, qty):
    ticker = client.get_orderbook_ticker(symbol=pair_symbol)
    print("Current bid price: {}".format(ticker.get('bidPrice')))
    print("Current ask price: {}".format(ticker.get('askPrice')))
    buy_price = float(ticker.get('bidPrice'))
    buy_price = price_accuracy % buy_price

    buy_order = client.create_margin_order(symbol=pair_symbol, 
                                       side=SIDE_BUY, 
                                       type=ORDER_TYPE_LIMIT,
                                       quantity=qty, 
                                       price=buy_price,
                                       timeInForce=TIME_IN_FORCE_GTC)

    logger.info("自动补仓代币 {}: {}, 补仓单价：{}".format(coin_symbol, qty, buy_price))


'''
purpose: 杠杆交易怕平仓，所以通过最简化的交易单数可以判断出是否超出仓位

'''
def is_max_margins(max_margins):
    orders = client.get_open_margin_orders(symbol=pair_symbol)
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