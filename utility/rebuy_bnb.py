# -*- coding: utf-8 -*-

from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
import time
from datetime import datetime

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from settings import BinanceKey1

api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']
client = Client(api_key, api_secret, {"verify": True, "timeout": 10000})

# 配置参数
symbol = 'BNBUSDT'
coin_symbol = 'BNB'
usdt_symbol = 'USDT'
bnb_symbol = 'BNB'
max_qty = 10

def run():
    print('='*30)
    print("\n购入{}，手续费需要 {} {}\n".format(coin_symbol, buy_qty, coin_symbol))
    repay_coin(max_qty)
    print("Done!")

def repay_coin(qty):
    ticker = client.get_orderbook_ticker(symbol=symbol)
    print("Current bid price: {}".format(ticker.get('bidPrice')))
    print("Current ask price: {}".format(ticker.get('askPrice')))
    buy_price = float(ticker.get('bidPrice'))
    buy_price = '%.4f' % buy_price


    buy_order = client.create_margin_order(symbol=symbol, 
                                       side=SIDE_BUY, 
                                       type=ORDER_TYPE_LIMIT,
                                       quantity=qty, 
                                       price=buy_price,
                                       timeInForce=TIME_IN_FORCE_GTC)
    
if __name__ == "__main__":
    run()