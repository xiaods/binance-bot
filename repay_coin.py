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
symbol = 'EOSUSDT'
coin_symbol = 'EOS'
usdt_symbol = 'USDT'
bnb_symbol = 'BNB'
max_margins = 15
# 投入本金，手工统计
base_balance = 1134
fiat_symbol = 'CNY'
fiat_price = 7.1

def run():
    print('='*30)
    print("\n购入{}，恢复Bot的最低风控阈值 for 60 {}".format(coin_symbol, coin_symbol))
    repay_coin(30)

def repay_coin(qty):
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
    
    # sell_order = client.create_margin_order(symbol=symbol, 
    #                                    side=SIDE_SELL, 
    #                                    type=ORDER_TYPE_LIMIT,
    #                                    quantity=10.0, 
    #                                    price=sell_price,
    #                                    timeInForce=TIME_IN_FORCE_GTC)


if __name__ == "__main__":
    run()