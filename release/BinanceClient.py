from binance .client import Client #line:3
from binance .enums import *#line:4
from binance .websockets import BinanceSocketManager #line:5
import time #line:6
from datetime import datetime #line:7
from BinanceKeys import BinanceKey1 #line:9
api_key =BinanceKey1 ['api_key']#line:11
api_secret =BinanceKey1 ['api_secret']#line:12
client =Client (api_key ,api_secret )#line:13
symbol ='EOSUSDT'#line:16
coin_symbol ='EOS'#line:17
usdt_symbol ='USDT'#line:18
bnb_symbol ='BNB'#line:19
max_margins =15 #line:20
base_balance =1134 #line:22
fiat_symbol ='CNY'#line:23
fiat_price =7.1 #line:24
def run ():#line:26
    print ('='*30 )#line:27
    get_account_status ()#line:28
def get_account_status ():#line:30
    O000O0O00O00OOO00 =client .get_avg_price (symbol ='BTCUSDT')#line:31
    OO000OO0000OO0OOO =client .get_avg_price (symbol ='BNBUSDT')#line:32
    OO00OO00O0O0O00O0 =float (O000O0O00O00OOO00 .get ('price'))#line:33
    O000OO0O00O0O00O0 =float (OO000OO0000OO0OOO .get ('price'))#line:34
    OO0O000OO000000O0 ="QCat Auto Trading bot\n"#line:35
    OO0O000OO000000O0 +="-"*30 #line:36
    OOOO000000O00000O =datetime .now ()#line:37
    OO0OOO00O000O0O00 =OOOO000000O00000O .strftime ("%Y-%m-%d %H:%M:%S")#line:38
    OO0O000OO000000O0 +="\n统计时间：%s"%OO0OOO00O000O0O00 #line:39
    OO0O000OO000000O0 +="\n当前BTC价格: {:.2f} USDT\n".format (OO00OO00O0O0O00O0 )#line:40
    OO0O000OO000000O0 +="当前BNB价格: {:.2f} USDT\n\n".format (O000OO0O00O0O00O0 )#line:41
    OOO000O00000000OO =client .get_margin_account ()#line:44
    O0O0O0O00O0O00000 =OOO000O00000000OO .get ('userAssets')#line:45
    O0OOO0000OO0O0OO0 =float (0 )#line:46
    O0OOOO0OOO0OOOOO0 =float (0 )#line:47
    OO0OOO0OOO000O0OO =float (0 )#line:48
    OO000O0O0OOO0OOOO =float (0 )#line:49
    OO0000OOOO0OOO0OO =float (0 )#line:50
    for OO00O0000000OOOO0 in O0O0O0O00O0O00000 :#line:51
        if OO00O0000000OOOO0 .get ('asset')==coin_symbol :#line:52
            O0OOO0000OO0O0OO0 =OO00O0000000OOOO0 .get ('free')#line:53
            OO0OOO0OOO000O0OO =OO00O0000000OOOO0 .get ('borrowed')#line:54
            OO000O0O0OOO0OOOO =OO00O0000000OOOO0 .get ('netAsset')#line:55
        if OO00O0000000OOOO0 .get ('asset')==bnb_symbol :#line:56
            OO0000OOOO0OOO0OO =OO00O0000000OOOO0 .get ('free')#line:57
        if OO00O0000000OOOO0 .get ('asset')==usdt_symbol :#line:58
            O0OOOO0OOO0OOOOO0 =OO00O0000000OOOO0 .get ('free')#line:59
    OO00OO00000O0OO0O =float (OO0000OOOO0OOO0OO )#line:63
    O0O0OOOO0OO00O0OO =float (base_balance )+float (OO00OO00000O0OO0O *O000OO0O00O0O00O0 )#line:64
    O0OOOOOO0000O0000 =(float (OOO000O00000000OO .get ("totalNetAssetOfBtc"))*OO00OO00O0O0O00O0 )-O0O0OOOO0OO00O0OO #line:66
    O0O0O0O000O0OOOO0 =float (O0OOOOOO0000O0000 /O0O0OOOO0OO00O0OO )#line:68
    OO0O000OO000000O0 +="*** 投入本金: {} USDT, {} BNB (约为{}: {:.2f}) ***\n".format (base_balance ,OO00OO00000O0OO0O ,fiat_symbol ,O0O0OOOO0OO00O0OO )#line:69
    OO0O000OO000000O0 +="*** 日累计盈亏: {0:.2f} USDT(约为{1}: {2:.2f} )，日利润率{3:.3%} ***\n\n".format (O0OOOOOO0000O0000 ,fiat_symbol ,float (O0OOOOOO0000O0000 *fiat_price ),O0O0O0O000O0OOOO0 )#line:70
    OO0O000OO000000O0 +="-"*30 #line:71
    OO0O000OO000000O0 +="\n杠杆账号资产详情：\n"#line:72
    OO0O000OO000000O0 +="\n当前杠杆账号风险率(默认3倍杠杆，小于2表示危险，需要人工处理): %s\n"%OOO000O00000000OO .get ("marginLevel")#line:73
    OO0O000OO000000O0 +="当前杠杆账号总资产估值: {0} BTC (约为 {1:.2f} USDT )\n".format (OOO000O00000000OO .get ("totalAssetOfBtc"),float (OOO000O00000000OO .get ("totalAssetOfBtc"))*OO00OO00O0O0O00O0 )#line:74
    OO0O000OO000000O0 +="当前杠杆账号账户权益: {0} BTC (约为 {1:.2f} USDT )\n".format (OOO000O00000000OO .get ("totalNetAssetOfBtc"),float (OOO000O00000000OO .get ("totalNetAssetOfBtc"))*OO00OO00O0O0O00O0 )#line:75
    OO0O000OO000000O0 +="当前帐户可用现金{0}是: {1}\n".format (usdt_symbol ,float (O0OOOO0OOO0OOOOO0 ))#line:77
    OO0O000OO000000O0 +="当前账户可用代币{0}是: {1}\n".format (coin_symbol ,float (O0OOO0000OO0O0OO0 ))#line:78
    print (OO0O000OO000000O0 )#line:79
    OO0000O00OO00O0O0 ="当前借入{}资产是{}\n".format (coin_symbol ,OO0OOO0OOO000O0OO )#line:80
    OO0000O00OO00O0O0 +="当前{}的净资产是{}\n".format (coin_symbol ,OO000O0O0OOO0OOOO )#line:81
    print (OO0000O00OO00O0O0 )#line:82
def get_free_assets ():#line:85
    OOOO0O00OO00OO0O0 =client .get_margin_account ()#line:86
    O00OOOO0000000OOO =OOOO0O00OO00OO0O0 .get ('userAssets')#line:87
    print ("free cash: %.4f "%float (free_cash ))#line:89
    print ("free coin: %.4f "%float (free_coin ))#line:90
def get_margin_stream_keepalive (O0OO0000OO0OO0OOO ):#line:92
    O00OO00O0O000000O =client .margin_stream_keepalive (O0OO0000OO0OO0OOO )#line:93
    print (O00OO00O0O000000O )#line:94
def get_margin_listen_key ():#line:97
    O00000OOOO00O0OO0 =client .margin_stream_get_listen_key ()#line:98
    print (O00000OOOO00O0OO0 )#line:99
def retry_websocket ():#line:101
    O00O0OO0000OO000O =BinanceSocketManager (client )#line:102
    O0000OOOO0O0O0O00 =O00O0OO0000OO000O .start_margin_socket (process_message )#line:103
    print ("websocket Conn key: "+O0000OOOO0O0O0O00 )#line:104
    O00O0OO0000OO000O .start ()#line:105
    time .sleep (1 )#line:106
    O00O0OO0000OO000O .stop_socket (O0000OOOO0O0O0O00 )#line:107
    O0000OOOO0O0O0O00 =O00O0OO0000OO000O .start_margin_socket (process_message )#line:108
    print ("renewer websocket Conn key: "+O0000OOOO0O0O0O00 )#line:109
def process_message (OOOO0O0OO0O000000 ):#line:111
    print (OOOO0O0OO0O000000 )#line:112
def is_max_margins (O00O000O0O0OOOOOO ):#line:114
    OOO00OO0O0O000OO0 =client .get_open_margin_orders (symbol =symbol )#line:115
    if len (OOO00OO0O0O000OO0 )>O00O000O0O0OOOOOO :#line:116
        return True #line:117
    else :#line:118
        return False #line:119
def loan_asset (O0OO0000O0O00OOO0 ,OO00OOOO0O0O0OOOO ):#line:121
    O00O0OO00OOOOO00O =client .get_margin_account ()#line:122
    O0OO000OOOO000OOO =O00O0OO00OOOOO00O .get ('userAssets')#line:123
    O0O0O0OOOO0000OO0 =float (0 )#line:124
    for O0O0000OOO00000OO in O0OO000OOOO000OOO :#line:125
        if O0O0000OOO00000OO .get ('asset')=='EOS':#line:126
            O0O0O0OOOO0000OO0 =float (O0O0000OOO00000OO .get ('borrowed'))#line:127
    OO00OOOO0O0O0OOOO =OO00OOOO0O0O0OOOO -O0O0O0OOOO0000OO0 #line:128
    if OO00OOOO0O0O0OOOO <=float (0 ):#line:129
        print ('don\'t need loan, original loan: {}'.format (O0O0O0OOOO0000OO0 ))#line:130
        pass #line:131
    else :#line:132
        OOO00OO0OO00O00OO =client .create_margin_loan (asset =O0OO0000O0O00OOO0 ,amount =OO00OOOO0O0O0OOOO )#line:134
        print (OOO00OO0OO00O00OO )#line:135
def repay_asset (OO0OOOOOOOOO0OO00 ,O000OOO0OOO0OO0O0 ):#line:137
    O0OO00OOOOO0O00O0 =client .repay_margin_loan (asset =OO0OOOOOOOOO0OO00 ,amount =O000OOO0OOO0OO0O0 )#line:139
    print (O0OO00OOOOO0O00O0 )#line:140
def get_all_margin_orders ():#line:142
    O00OO0OO000O0O0O0 =client .get_open_margin_orders (symbol =symbol )#line:143
    print (O00OO0OO000O0O0O0 )#line:144
def cacel_all_margin_orders ():#line:146
    O0OOOOOOOOOO000OO =client .get_open_margin_orders (symbol =symbol )#line:147
    for OO00OOOO00O00000O in O0OOOOOOOOOO000OO :#line:148
        O0OOOO000OOO0OO0O =client .cancel_margin_order (symbol =symbol ,orderId =OO00OOOO00O00000O .get ('orderId'))#line:150
        print (O0OOOO000OOO0OO0O )#line:151
def margin_account ():#line:153
    OO00000OOOOOOOO0O =client .get_margin_account ()#line:154
    O000OOO00O0O0000O =OO00000OOOOOOOO0O .get ('userAssets')#line:155
    for OOOO0OOOOOOO0OOOO in O000OOO00O0O0000O :#line:156
        if OOOO0OOOOOOO0OOOO .get ('asset')==coin_symbol :#line:157
            OO0OO0OO00O0O0000 =OOOO0OOOOOOO0OOOO .get ('free')#line:158
        if OOOO0OOOOOOO0OOOO .get ('asset')==usdt_symbol :#line:159
            O0O0O0O0OOOO0O0O0 =OOOO0OOOOOOO0OOOO .get ('free')#line:160
    print (OO0OO0OO00O0O0000 ,O0O0O0O0OOOO0O0O0 )#line:162
def new_margin_order ():#line:164
    O0O0OOO0O000O000O =client .get_orderbook_ticker (symbol =symbol )#line:165
    print ("Current bid price: {}".format (O0O0OOO0O000O000O .get ('bidPrice')))#line:166
    print ("Current ask price: {}".format (O0O0OOO0O000O000O .get ('askPrice')))#line:167
    OO0OO0OOO000OOO0O =float (O0O0OOO0O000O000O .get ('bidPrice'))*float (1 -0.005 )#line:168
    OO0OO0OOO000OOO0O ='%.4f'%OO0OO0OOO000OOO0O #line:169
    O00O0O000O000O0OO =float (O0O0OOO0O000O000O .get ('askPrice'))*float (1 +0.005 )#line:171
    O00O0O000O000O0OO ='%.4f'%O00O0O000O000O0OO #line:172
    O000000OO0OO00000 =client .create_margin_order (symbol =symbol ,side =SIDE_BUY ,type =ORDER_TYPE_LIMIT ,quantity =10.0 ,price =OO0OO0OOO000OOO0O ,timeInForce =TIME_IN_FORCE_GTC )#line:179
    O00O00OO00O0000OO =client .create_margin_order (symbol =symbol ,side =SIDE_SELL ,type =ORDER_TYPE_LIMIT ,quantity =10.0 ,price =O00O0O000O000O0OO ,timeInForce =TIME_IN_FORCE_GTC )#line:186
if __name__ =="__main__":#line:188
    run ()