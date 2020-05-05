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

def run():
    print('='*30)
    print("获取划转历史 (USER_DATA)")
    result = get_margin_transfer()
    print(result)

def get_margin_transfer():
    '''
    not yet implemented
    '''
    return "TODO"
    
if __name__ == "__main__":
    run()