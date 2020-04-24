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

from BinanceKeys import BinanceKey1
api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']
client = Client(api_key, api_secret)

def run():
    initialize_arb()

def initialize_arb():
    welcome_message = "\n\n---------------------------------------------------------\n\n"
    welcome_message+= "Binance auto trading bot\n"
    bot_start_time = str(datetime.now())
    welcome_message+= "\nBot Start Time: {}\n\n\n".format(bot_start_time)
    print(welcome_message)
    time.sleep(1)
    try:
        status = client.get_system_status()
        print("\nExchange Status: ", status)
        symbol = 'EOSUSDT'
        tickers = client.get_orderbook_ticker(symbol=symbol)
        print(tickers)
        # while True:


    except:
        print("\nFAILURE INITIALIZE\n")
        raise

if __name__ == "__main__":
    run()