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