# -*- coding: utf-8 -*-

from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
import time
from datetime import datetime

from settings import MarginAccount
from BinanceKeys import BinanceKey1
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
    get_account_status()

def get_account_status():
    btcusdt_avg_price = client.get_avg_price(symbol='BTCUSDT')
    bnbusdt_avg_price = client.get_avg_price(symbol='BNBUSDT')
    current_btc_price = float(btcusdt_avg_price.get('price'))
    current_bnb_price = float(bnbusdt_avg_price.get('price'))
    message = "QCat Auto Trading bot\n"
    message += "-"*30 
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    message += "\n统计时间：%s" % dt_string
    message += "\n当前BTC价格: {:.2f} USDT\n".format(current_btc_price)
    message += "当前BNB价格: {:.2f} USDT\n\n".format(current_bnb_price)

    # 计算账户信息 start
    account = client.get_margin_account()
    userAssets = account.get('userAssets')
    free_coin = float(0)
    free_cash = float(0)
    loan_coin = float(0)
    net_coin = float(0)
    bnb_free_coin = float(0)
    for asset in userAssets:
        if asset.get('asset') == coin_symbol:
            free_coin = asset.get('free')
            loan_coin = asset.get('borrowed')
            net_coin = asset.get('netAsset')
        if asset.get('asset') == bnb_symbol:
            bnb_free_coin = asset.get('free')
        if asset.get('asset') == usdt_symbol:
            free_cash = asset.get('free')
    # 计算账号信息 end

    # 总投入成本
    base_bnb_balance = float(bnb_free_coin)
    total_base_balance = float(base_balance) + float(base_bnb_balance * current_bnb_price)
    # 利润
    profit_balance = (float(account.get("totalNetAssetOfBtc")) *  current_btc_price) - total_base_balance
    # 利润率
    profit_percent = float(profit_balance / total_base_balance)
    message += "*** 投入本金: {} USDT, {} BNB (约为{}: {:.2f}) ***\n".format(base_balance, base_bnb_balance, fiat_symbol, total_base_balance * fiat_price)
    message += "*** 日累计盈亏: {0:.2f} USDT(约为{1}: {2:.2f} )，日利润率{3:.3%} ***\n\n".format(profit_balance, fiat_symbol, float(profit_balance * fiat_price), profit_percent)
    message += "-"*30
    message += "\n杠杆账号资产详情：\n"
    message += "\n当前杠杆账号风险率(默认3倍杠杆，小于2表示危险，需要人工处理): %s\n"  % account.get("marginLevel")
    message += "当前杠杆账号总资产估值: {0} BTC (约为 {1:.2f} USDT )\n".format( account.get("totalAssetOfBtc"), float(account.get("totalAssetOfBtc")) *  current_btc_price )
    message += "当前杠杆账号账户权益: {0} BTC (约为 {1:.2f} USDT )\n".format( account.get("totalNetAssetOfBtc"), float(account.get("totalNetAssetOfBtc")) * current_btc_price  )

    message += "当前帐户可用现金{0}是: {1}\n".format(usdt_symbol, float(free_cash) ) 
    message += "当前账户可用代币{0}是: {1}\n".format(coin_symbol, float(free_coin) )
    print(message)
    asset_message = "当前借入{}资产是{}\n".format(coin_symbol, loan_coin)
    asset_message += "当前{}的净资产是{}\n".format(coin_symbol, net_coin)
    print(asset_message)


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