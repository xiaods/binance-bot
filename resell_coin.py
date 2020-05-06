# -*- coding: utf-8 -*-

from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
import time
from datetime import datetime

from settings import BinanceKey1

api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']
client = Client(api_key, api_secret)

# 配置参数
symbol = 'EOSUSDT'
coin_symbol = 'EOS'
usdt_symbol = 'USDT'
bnb_symbol = 'BNB'
max_margins = 15

def run():
    print('='*30)
    print("\n卖出{}，恢复Bot的最低风控阈值 >= 60 {}\n".format(coin_symbol, coin_symbol))
    repay_coin(40)
    print("Done!")

def repay_coin(qty):
    ticker = client.get_orderbook_ticker(symbol=symbol)
    print("Current bid price: {}".format(ticker.get('bidPrice')))
    print("Current ask price: {}".format(ticker.get('askPrice')))

    sell_price = float(ticker.get('askPrice'))
    sell_price = '%.4f' % sell_price
    
    sell_order = client.create_margin_order(symbol=symbol, 
                                       side=SIDE_SELL, 
                                       type=ORDER_TYPE_LIMIT,
                                       quantity=qty, 
                                       price=sell_price,
                                       timeInForce=TIME_IN_FORCE_GTC)

if __name__ == "__main__":
    run()