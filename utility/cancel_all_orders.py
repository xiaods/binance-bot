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
symbol = 'EOSUSDT'
coin_symbol = 'EOS'
usdt_symbol = 'USDT'
bnb_symbol = 'BNB'

def run():
    print('='*30)
    
    cancel_all_margin_orders(symbol)
    print("Done!")

def cancel_all_margin_orders(symbol):
    orders = client.get_open_margin_orders(symbol=symbol)
    print("取消挂单：\n")

    for o in orders:
        result = client.cancel_margin_order(symbol=symbol,
                                            orderId=o.get('orderId'))
        print("{}".format(result))


if __name__ == "__main__":
    run()