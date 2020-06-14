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
    'loan_balance': 0,   # <-----借贷币的数量
    'loan_enabled': False,  #<------是否借币开关，在币价动荡的时候，可以关闭借币通道
    'coin_balance': 0, #<----- 开盘总持有币数量
    'depth': 1,   # <-----对手单深度数
    'bnb_symbol': 'BNB',
    'base_balance': 0,  # <---投入本金，一般为USDT
    'base_bnb_balance': 0, # <---投入BNB，当手续费使用，在千1手续费之上打75折
    'fiat_symbol': 'USD',  # <---本地法币
    'fiat_price': 1,   # 1 USD 兑换 本地法币的价格
    'max_margins': 20,  # <--------(depth * 2) * float(0.8), 最大交易对数量
    'free_cash_limit_percentile': 0.1,  #<-----最小可用金额百分比， 20%
    'price_accuracy': '%.4f',  #<----- 价格精度，交易需要指定。默认 .4f
    'qty_accuracy': '%.2f', #<------ 数量进度， EOS是 2个， BTC是6个
    'trend_limit_tan': [0.1763, -0.1763],  #<--------- 趋势判断，kline 用tan函数，默认是tan10, 但是EOS比值太小，换了更小的值
 }

BinanceKey1 = {'api_key': '< your api key>',
    'api_secret':'< your api secret>'}