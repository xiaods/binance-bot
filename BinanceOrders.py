# -*- coding: utf-8 -*-

from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
import time
from datetime import datetime
import prettytable as pt
from settings import MarginAccount

from settings import BinanceKey1

api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']
client = Client(api_key, api_secret)

# 配置参数
symbol = MarginAccount['pair_symbol']
coin_symbol = MarginAccount['eos_symbol']
usdt_symbol = MarginAccount['usdt_symbol']
bnb_symbol = MarginAccount['bnb_symbol']
max_margins = 15
# 投入本金，手工统计
base_balance = MarginAccount['base_balance']
fiat_symbol = MarginAccount['fiat_symbol']
fiat_price = MarginAccount['fiat_price']

def run():
    print('='*30)
    get_all_margin_orders()


def get_all_margin_orders():
    orders = client.get_open_margin_orders(symbol=symbol)
    
    tb = pt.PrettyTable()
    tb.field_names = ["orderId", "Qty", "Price", "Side","Symbol", "Time"]
    for o in orders:
        tb.add_row([ o["orderId"], o["origQty"], o["price"], o["side"], o["symbol"], timestamp2string(o["time"]) ])

    print(tb)


def timestamp2string(timeStamp):
    try:
        d = datetime.fromtimestamp(int(timeStamp)/1000)
        dtstr = d.strftime("%Y-%m-%d %H:%M:%S")
        return dtstr
    except Exception as e:
        print(e)
        return ''

if __name__ == "__main__":
    run()