# -*- coding: utf-8 -*-

"""
Binance bot all settings
"""

ZohoMail = {'username': 'support@qcat.io',
    'password':'< your password >',
    'smtpserver': '< smtp server>',
    'serverport': 465,
    'recipient': [' <recipient email>'],
    }

MarginAccount = {
    'pair_symbol': 'EOSUSDT',
    'coin_symbol': 'EOS',
    'usdt_symbol': 'USDT',
    'loan': 0,   # <-----借贷币的数量
    'depth': 1,   # <-----对手单深度数
    'bnb_symbol': 'BNB',
    'base_balance': 0,  # <---投入本金，一般为USDT
    'base_bnb_balance': 0, # <---投入BNB，当手续费使用，在千1手续费之上打75折
    'fiat_symbol': 'USD',  # <---本地法币
    'fiat_price': 1,   # 1 USD 兑换 本地法币的价格
    'max_margins': 20,  # <--------(depth * 2) * float(0.8), 最大交易对数量
    'free_coin_limit_percentile': 0.1,  #<-----最小可用币数量百分比， 20%
    'free_cash_limit_percentile': 0.1,  #<-----最小可用金额百分比， 20%
    'price_accuracy': '%.4f',  #<----- 价格精度，交易需要指定。默认 .4f
 }

BinanceKey1 = {'api_key': '< your api key>',
    'api_secret':'< your api secret>'}