# -*- coding: utf-8 -*-

from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
import time

from BinanceKeys import BinanceKey1

api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']
client = Client(api_key, api_secret)

symbol = 'EOSUSDT'
coin_symbol = 'EOS'
usdt_symbol = 'USDT'
max_margins = 15

def run():
    print('=========start running=================')

    print("current orders")
    get_all_margin_orders()

    print('current free assets')
    get_free_assets()

def get_free_assets():
    account = client.get_margin_account()
    userAssets = account.get('userAssets')
    free_coin = float(0)
    free_cash = float(0)
    for asset in userAssets:
        if asset.get('asset') == coin_symbol:
            free_coin = asset.get('free')
        if asset.get('asset') == usdt_symbol:
            free_cash = asset.get('free')
    print("free cash: %.4f " % float(free_cash) )
    print("free coin: %.4f " % float(free_coin) )

def get_margin_stream_keepalive(listen_key):
    result = client.margin_stream_keepalive(listen_key)
    print(result)

# get listen key for websocket
def get_margin_listen_key():
    key = client.margin_stream_get_listen_key()
    print(key)

def retry_websocket():
    bm = BinanceSocketManager(client)
    conn_key = bm.start_margin_socket(process_message)
    print("websocket Conn key: " + conn_key)
    bm.start()
    time.sleep(1)
    bm.stop_socket(conn_key)
    conn_key = bm.start_margin_socket(process_message)
    print("renewer websocket Conn key: " + conn_key)

def process_message(msg):
    print(msg)

def is_max_margins(max_margins):
    orders = client.get_open_margin_orders(symbol=symbol)
    if len(orders) > max_margins:
        return True
    else:
        return False

def loan_asset(coin_symbol, qty):
    account = client.get_margin_account()
    userAssets = account.get('userAssets')
    origin_loan = float(0)
    for asset in userAssets:
        if asset.get('asset') == 'EOS':
            origin_loan = float(asset.get('borrowed'))
    qty = qty - origin_loan
    if qty <= float(0):
        print('don\'t need loan, original loan: {}'.format(origin_loan))
        pass
    else:
        transaction = client.create_margin_loan(asset=coin_symbol, 
                                            amount=qty)
        print(transaction)

def repay_asset(coin_symbol, qty):
    transaction = client.repay_margin_loan(asset=coin_symbol, 
                                            amount=qty)
    print(transaction)

def get_all_margin_orders():
    orders = client.get_open_margin_orders(symbol=symbol)
    print(orders)

def cacel_all_margin_orders():
    orders = client.get_open_margin_orders(symbol=symbol)
    for o in orders:
        result = client.cancel_margin_order(symbol=symbol,
                                            orderId=o.get('orderId'))
        print(result)

def margin_account():
    account = client.get_margin_account()
    userAssets = account.get('userAssets')
    for asset in userAssets:
        if  asset.get('asset') == coin_symbol:
            eos_free = asset.get('free')
        if  asset.get('asset') == usdt_symbol:
            usdt_free = asset.get('free')

    print(eos_free, usdt_free)

def new_margin_order():
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
                                       quantity=10.0, 
                                       price=buy_price,
                                       timeInForce=TIME_IN_FORCE_GTC)
    
    sell_order = client.create_margin_order(symbol=symbol, 
                                       side=SIDE_SELL, 
                                       type=ORDER_TYPE_LIMIT,
                                       quantity=10.0, 
                                       price=sell_price,
                                       timeInForce=TIME_IN_FORCE_GTC)

if __name__ == "__main__":
    run()