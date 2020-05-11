# -*- coding: utf-8 -*-

from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
import time
from datetime import datetime

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from settings import BinanceKey1
from settings import MarginAccount

api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']
client = Client(api_key, api_secret, {"verify": True, "timeout": 10000})

# 配置参数
loan_qty = MarginAccount['loan']
coin_symbol = MarginAccount['coin_symbol']


def run():
    print('='*30)
    print("\n归还loan {} {}\n".format(coin_symbol, loan_qty))
    repay_loan(coin_symbol, loan_qty)
    print("Done!")

def repay_loan(coin_symbol, qty):
    transaction = client.repay_margin_loan(asset=coin_symbol, 
                                            amount=qty)
    print(transaction)

if __name__ == "__main__":
    run()