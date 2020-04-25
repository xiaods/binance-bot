# -*- coding: utf-8 -*-
"""
币安自动交易bot
Python-Binance ( https://github.com/sammchardy/python-binance )
pip install python-binance  (note: support python3)

"""

from binance.client import Client
from binance.enums import *
import time
from datetime import datetime
from binance.websockets import BinanceSocketManager

import os
import sys
import signal

from BinanceKeys import BinanceKey1
api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']
client = Client(api_key, api_secret)

# step0 初始化变化
symbol = 'EOSUSDT'
eos_symbol = 'EOS'
loan = 200
depth = 10
qty = loan / depth
max_margins = (depth * 2) * (0.5)

def run():
    initialize_arb()

def initialize_arb():
    welcome_message = "\n\n---------------------------------------------------------\n\n"
    welcome_message+= "Binance auto trading bot\n"
    bot_start_time = str(datetime.now())
    welcome_message+= "\nBot Start Time: {}\n\n\n".format(bot_start_time)
    print(welcome_message)
    time.sleep(1)
    status = client.get_system_status()
    print("\nExchange Status: ", status)

    # step1 创建对手单,第一入口
    cancel_all_margin_orders(symbol)
    loan_asset(eos_symbol,loan)
    new_margin_order(symbol,qty)

    # step2 监听杠杆交易
    global bm
    bm = BinanceSocketManager(client, user_timeout=60)
    conn_key = bm.start_margin_socket(process_message)
    print("websocket Conn key: " + conn_key)
    bm.start()

def new_margin_order(symbol,qty):
    ticker = client.get_orderbook_ticker(symbol=symbol)
    print("Current bid price: {}".format(ticker.get('bidPrice')))
    print("Current ask price: {}".format(ticker.get('askPrice')))
    buy_price = float(ticker.get('bidPrice'))*float(1-0.005)
    buy_price = '%.4f' % buy_price

    sell_price = float(ticker.get('askPrice'))*float(1+0.005)
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

def cancel_all_margin_orders(symbol):
    orders = client.get_open_margin_orders(symbol=symbol)
    for o in orders:
        result = client.cancel_margin_order(symbol=symbol,
                                            orderId=o.get('orderId'))
        print(result)

def is_max_margins(max_margins):
    orders = client.get_open_margin_orders(symbol=symbol)
    if len(orders) > max_margins:
        return True
    else:
        return False

def loan_asset(eos_symbol, qty):
    transaction = client.create_margin_loan(asset=eos_symbol, 
                                            amount=qty)
    print(transaction)

def process_message(msg):
    print(msg)

    if is_max_margins(max_margins) == True:
        cancel_all_margin_orders(symbol)

    # 处理event executionReport
    if msg.get('e') == 'executionReport' and msg.get('s')  == symbol and msg.get('x') == 'TRADE':
        new_margin_order(symbol,qty)

def term_sig_handler(signum, frame):
    print('catched singal: %d' % signum)
    bm.close()
    sys.exit()

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, term_sig_handler)
    signal.signal(signal.SIGINT, term_sig_handler)
    signal.signal(signal.SIGHUP, term_sig_handler)
    run()