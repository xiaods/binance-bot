# -*- coding: utf-8 -*-

from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
import time
from datetime import datetime

from BinanceKeys import BinanceKey1

api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']
client = Client(api_key, api_secret)

# 配置参数
loan_qty=20
coin_symbol = 'EOS'


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