# -*- coding: utf-8 -*-
"""
币安自动交易bot
Python-Binance ( https://github.com/sammchardy/python-binance )
pip install python-binance  (note: support python3)

"""
import time
from datetime import datetime
import sys
import signal

import logging
from logging.handlers import TimedRotatingFileHandler
import re

from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor

from settings import MarginAccount

from settings import BinanceKey1
API_KEY = BinanceKey1['api_key']
API_SECRET = BinanceKey1['api_secret']
client = Client(API_KEY, API_SECRET)

# logger初始化

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

# step0 初始化参数，请咨询核对调优
symbol = MarginAccount['pair_symbol']
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
    # 1.1 清空当前交易
    cancel_all_margin_orders(symbol)
    # 1.2 借出币
    loan_asset(eos_symbol,loan)
    # 创建新的交易
    new_margin_order(symbol,qty)

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

def new_margin_order(symbol,qty):

    # 当前报价口的买卖价格
    ticker = client.get_orderbook_ticker(symbol=symbol)
    logger.info("Current bid price: {}".format(ticker.get('bidPrice')))
    logger.info("Current ask price: {}".format(ticker.get('askPrice')))
    buy_price = float(ticker.get('bidPrice'))*float(1-0.005)
    buy_price = '%.4f' % buy_price

    sell_price = float(ticker.get('askPrice'))*float(1+0.005)
    sell_price = '%.4f' % sell_price

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

def cancel_all_margin_orders(symbol):
    orders = client.get_open_margin_orders(symbol=symbol)
    logger.info("取消挂单：\n")

    for o in orders:
        result = client.cancel_margin_order(symbol=symbol,
                                            orderId=o.get('orderId'))
        logger.info("{}".format(result))


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
        if asset.get('asset') == 'EOS':
            origin_loan = float(asset.get('borrowed'))
    qty = qty - origin_loan
    if qty <= float(0):
        logger.info('don\'t need loan, original loan: {}'.format(origin_loan))
        pass
    else:
        transaction = client.create_margin_loan(asset=eos_symbol,
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
        if msg.get('e') == 'executionReport' and msg.get('s')  == symbol:
            logger.info(msg)
        # 当有交易成功的挂单，挂起新的网格对手单
        if msg.get('e') == 'executionReport' and msg.get('s')  == symbol and msg.get('X') == ORDER_STATUS_FILLED:
            new_margin_order(symbol,qty)

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