# -*- coding: utf-8 -*-
"""
币安自动交易bot
    KDJ + Bollinger Close Price边界跨过布林线后，通过KDJ的金叉给一个捕鱼信号。每次只出一单。
"""
import time
from datetime import datetime
import sys
import signal

import logging
from logging.handlers import TimedRotatingFileHandler
import re

import pandas as pd
import talib
from talib import MA_Type
import numpy as np #computing multidimensionla arrays

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

logger = logging.getLogger("kdj_bollinger_bot")

log_format = "%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(filename)s[line:%(lineno)d] %(message)s"
log_level = 10
handler = TimedRotatingFileHandler("kdj_bollinger_bot.log", when="midnight", interval=1)
handler.setLevel(log_level)
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
handler.suffix = "%Y%m%d"
handler.extMatch = re.compile(r"^\d{8}$") 
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# step0 初始化参数，请咨询核对调优
pair_symbol = MarginAccount['pair_symbol']
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
# 数量进度
qty_accuracy = MarginAccount['qty_accuracy']

# BinanceSocketManager 全局变量初始化
bm = None
conn_key = None
indicator = None
#memory order dict
long_order = {}
short_order = {}

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

    # step1 第一入口
    # 1.2 借出币
    loan_asset(coin_symbol,loan)

    # step2 监听杠杆交易
    global bm, conn_key
    bm = BinanceSocketManager(client)
    conn_key = bm.start_margin_socket(process_message)
    logger.info("websocket Conn key: {}".format(conn_key) )
    bm.start()

    # 30分钟ping user websocket，key可以存活1个小时
    # 根据KDJ线 + Bolling线
    while True:
        get_margin_stream_keepalive(conn_key)
        kdj_signal_trading(pair_symbol)
        time.sleep(5)

"""
 KDJ + bollinger_signal 自动交易策略
 bollinger_signal 21,2
"""
def kdj_signal_trading(symbol):
    fastk_period = 9
    slowk_period = 3
    slowd_period = 3

    candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE)
    df = pd.DataFrame(candles)
    df.columns=['timestart','open','high','low','close','?','timeend','?','?','?','?','?']
    df.timestart = [datetime.fromtimestamp(i/1000) for i in df.timestart.values]
    df.timeend = [datetime.fromtimestamp(i/1000) for i in df.timeend.values]


    low_list = df['low'].rolling(9, min_periods=9).min()
    low_list.fillna(value = df['low'].expanding().min(), inplace = True)
    high_list = df['high'].rolling(9, min_periods=9).max()
    high_list.fillna(value = df['high'].expanding().max(), inplace = True)

    # Close price
    close_data = [float(x) for x in df.close.values]
    np_close_data = np.array(close_data)
    rsv = (np_close_data - low_list) / (high_list - low_list) * 100

    #high price
    high_data = [float(x) for x in df.high.values]
    np_high_data = np.array(high_data)

    #low price
    low_data = [float(x) for x in df.low.values]
    np_low_data = np.array(low_data)

    #Bollinger range
    up,mid,down=talib.BBANDS(np_close_data,21,nbdevup=2,nbdevdn=2)
    cur_up = up[-1]
    cur_md = mid[-1]
    cur_dn = down[-1]

    logger.info("Bollinger: up: {:.2f}, mid: {:.2f}, down: {:.2f}".format(up[-1],mid[-1],down[-1]))

    df['K'] = pd.DataFrame(rsv).ewm(com=2).mean()
    df['D'] = df['K'].ewm(com=2).mean()
    df['J'] = 3 * df['K'] - 2 * df['D']
    np_k = np.array(df['K'])
    np_d = np.array(df['D'])
    np_j = np.array(df['J'])

    logger.info("KDJ: k: {:.2f}, d: {:.2f}, j: {:.2f}".format(np_k[-1],np_d[-1],np_j[-1]))
    # 交易策略，吃多单
    if (int(np_k[-1]) - int(np_d[-1])) in range(-2, 2) and \
        int(np_low_data[-1]) <= int(cur_dn) and len(long_order) == 0:
        indicator = "LONG"  #做多
        new_margin_order(symbol,qty)  #  下单
    elif (int(np_k[-1]) - int(np_d[-1])) in range(-2, 2) and \
        int(np_high_data[-1]) >= int(cur_up) and len(short_order) == 0:
        indicator = "SHORT" #做空
        new_margin_order(symbol,qty)  #  下单
    else:
        indicator = "NORMAL"   #正常网格, bypass
    


"""
下单函数，做空，做多
"""
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
    if free_coin < (loan * free_coin_limit_percentile):
        logger.warning("Current Account coin balance is less then {}%. don't do order anymore.".format(free_coin_limit_percentile * 100))
        buy_coin_qty = float(qty_accuracy % float(loan * 0.5))
        if free_cash > (base_balance * free_cash_limit_percentile) and (buy_coin_qty * float(buy_price)) < free_cash:
            repay_asset(pair_symbol, coin_symbol, buy_coin_qty, SIDE_BUY)
        return
    if free_cash < (base_balance * free_cash_limit_percentile):
        logger.warning("Current Account cash balance is less then {}%. don't do order anymore.".format(free_cash_limit_percentile * 100))
        sell_coin_qty = float(qty_accuracy % float(free_coin - loan))
        if free_coin > loan and (sell_coin_qty * float(sell_price)) > 10:  # 币安要求最小交易金额必须大于10
            repay_asset(pair_symbol, coin_symbol, sell_coin_qty, SIDE_SELL)
        return

   # LONG or SHORT
    if indicator == "LONG":
        buy_price = float(ticker.get('bidPrice'))*float(1)
        buy_price = price_accuracy % buy_price

        sell_price = float(ticker.get('askPrice'))*float(1+0.01)
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

        logger.info("做多：买单ID:{}, 价格：{}， 数量：{}".format(buy_order, buy_price, qty))
        logger.info("做多：卖单ID:{}, 价格：{}， 数量：{}".format(sell_order, sell_price, qty)) 
        long_order[SIDE_BUY] = buy_order.get("orderId")
        long_order[SIDE_SELL] = sell_order.get("orderId")

    elif indicator == "SHORT":
        sell_price = float(ticker.get('askPrice'))*float(1)
        sell_price = price_accuracy % sell_price

        buy_price = float(ticker.get('bidPrice'))*float(1-0.01)
        buy_price = price_accuracy % buy_price

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

        logger.info("做空：买单ID:{}, 价格：{}， 数量：{}".format(buy_order, buy_price, qty))
        logger.info("做空：卖单ID:{}, 价格：{}， 数量：{}".format(sell_order, sell_price, qty)) 
        short_order[SIDE_BUY] = buy_order.get("orderId")
        short_order[SIDE_SELL] = sell_order.get("orderId")

    else:
        logger.info("NO CHANCE: indicator:{}".format(indicator))

'''
purpose: coin补仓, 提供50%的币的数量
'''
def repay_asset(pair_symbol, coin_symbol, qty, type):
    ticker = client.get_orderbook_ticker(symbol=pair_symbol)
    print("Current bid price: {}".format(ticker.get('bidPrice')))
    print("Current ask price: {}".format(ticker.get('askPrice')))

    if type == SIDE_BUY:
        buy_price = float(ticker.get('bidPrice'))
        buy_price = price_accuracy % buy_price

        buy_order = client.create_margin_order(symbol=pair_symbol, 
                                       side=SIDE_BUY, 
                                       type=ORDER_TYPE_LIMIT,
                                       quantity=qty, 
                                       price=buy_price,
                                       timeInForce=TIME_IN_FORCE_GTC)

        logger.info("自动补仓代币 {}: {}, 补仓单价：{}".format(coin_symbol, qty, buy_price))
    elif type ==  SIDE_SELL:
        sell_price = float(ticker.get('askPrice'))
        sell_price = price_accuracy % sell_price
    
        sell_order = client.create_margin_order(symbol=pair_symbol, 
                                       side=SIDE_SELL, 
                                       type=ORDER_TYPE_LIMIT,
                                       quantity=qty, 
                                       price=sell_price,
                                       timeInForce=TIME_IN_FORCE_GTC)
        logger.info("自动兑换代币 {}: {}, 兑换单价：{}".format(coin_symbol, qty, sell_price))

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
def loan_asset(coin_symbol, qty):
    account = client.get_margin_account()
    userAssets = account.get('userAssets')
    origin_loan = float(0)
    for asset in userAssets:
        if asset.get('asset') == coin_symbol:
            origin_loan = float(asset.get('borrowed'))
    qty = qty - origin_loan
    if qty <= float(0):
        logger.info('don\'t need loan, original loan: {}'.format(origin_loan))
        pass
    else:
        transaction = client.create_margin_loan(asset=coin_symbol,
                                            amount=qty)
        logger.info(transaction)

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
        # 当有交易成功的挂单，更新交易对字典
        # "i": 4293153,                  // orderId
        # "S": "BUY",                    // 订单方向
        if msg.get('e') == 'executionReport' and msg.get('s')  == pair_symbol and msg.get('X') == ORDER_STATUS_FILLED:
            if msg.get('S') == SIDE_BUY and msg.get('i') == short_order.get(SIDE_BUY):
                del short_order[SIDE_BUY]
            elif msg.get('S') == SIDE_BUY and msg.get('i') == long_order.get(SIDE_BUY):
                del long_order[SIDE_BUY]
            elif msg.get('S') == SIDE_SELL and msg.get('i') == short_order.get(SIDE_SELL):
                del short_order[SIDE_SELL]
            elif msg.get('S') == SIDE_SELL and msg.get('i') == long_order.get(SIDE_SELL):
                del long_order[SIDE_SELL]

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