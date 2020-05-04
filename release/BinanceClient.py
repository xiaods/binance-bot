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
    OOO00OOO000OO000O =client .get_avg_price (symbol ='BTCUSDT')#line:31
    OOO0OO0OOO0OOOO0O =client .get_avg_price (symbol ='BNBUSDT')#line:32
    OOOOOO0O00O0OOOOO =float (OOO00OOO000OO000O .get ('price'))#line:33
    O0O0OO0OOOO0OO0O0 =float (OOO0OO0OOO0OOOO0O .get ('price'))#line:34
    O0OO0000O0000OOO0 ="QCat Auto Trading bot\n"#line:35
    O0OO0000O0000OOO0 +="-"*30 #line:36
    O00O00O000OO0OO0O =datetime .now ()#line:37
    OO0O00OOO0OO0O000 =O00O00O000OO0OO0O .strftime ("%Y-%m-%d %H:%M:%S")#line:38
    O0OO0000O0000OOO0 +="\n统计时间：%s"%OO0O00OOO0OO0O000 #line:39
    O0OO0000O0000OOO0 +="\n当前BTC价格: {:.2f} USDT\n".format (OOOOOO0O00O0OOOOO )#line:40
    O0OO0000O0000OOO0 +="当前BNB价格: {:.2f} USDT\n\n".format (O0O0OO0OOOO0OO0O0 )#line:41
    O0OO0O00OO0000OOO =client .get_margin_account ()#line:44
    O00O000OOO00O0OO0 =O0OO0O00OO0000OOO .get ('userAssets')#line:45
    OO0OO0OO00OOOOO0O =float (0 )#line:46
    OOOO0O0OOO0O00OOO =float (0 )#line:47
    O00O0O00000O0OOO0 =float (0 )#line:48
    O0O0000O00OOOO000 =float (0 )#line:49
    OO00O0OOOOO00000O =float (0 )#line:50
    for O0OOOOO0OO0O00000 in O00O000OOO00O0OO0 :#line:51
        if O0OOOOO0OO0O00000 .get ('asset')==coin_symbol :#line:52
            OO0OO0OO00OOOOO0O =O0OOOOO0OO0O00000 .get ('free')#line:53
            O00O0O00000O0OOO0 =O0OOOOO0OO0O00000 .get ('borrowed')#line:54
            O0O0000O00OOOO000 =O0OOOOO0OO0O00000 .get ('netAsset')#line:55
        if O0OOOOO0OO0O00000 .get ('asset')==bnb_symbol :#line:56
            OO00O0OOOOO00000O =O0OOOOO0OO0O00000 .get ('free')#line:57
        if O0OOOOO0OO0O00000 .get ('asset')==usdt_symbol :#line:58
            OOOO0O0OOO0O00OOO =O0OOOOO0OO0O00000 .get ('free')#line:59
    O0O000O0OOOOOOOO0 =float (OO00O0OOOOO00000O )#line:63
    O0O00000OOOOOO0O0 =float (base_balance )+float (O0O000O0OOOOOOOO0 *O0O0OO0OOOO0OO0O0 )#line:64
    OOOO0O0O00O0000O0 =(float (O0OO0O00OO0000OOO .get ("totalNetAssetOfBtc"))*OOOOOO0O00O0OOOOO )-O0O00000OOOOOO0O0 #line:66
    O0O0O000OOO0OO0O0 =float (OOOO0O0O00O0000O0 /O0O00000OOOOOO0O0 )#line:68
    O0OO0000O0000OOO0 +="*** 投入本金: {} USDT, {} BNB (约为{}: {:.2f}) ***\n".format (base_balance ,O0O000O0OOOOOOOO0 ,fiat_symbol ,O0O00000OOOOOO0O0 *fiat_price )#line:69
    O0OO0000O0000OOO0 +="*** 日累计盈亏: {0:.2f} USDT(约为{1}: {2:.2f} )，日利润率{3:.3%} ***\n\n".format (OOOO0O0O00O0000O0 ,fiat_symbol ,float (OOOO0O0O00O0000O0 *fiat_price ),O0O0O000OOO0OO0O0 )#line:70
    O0OO0000O0000OOO0 +="-"*30 #line:71
    O0OO0000O0000OOO0 +="\n杠杆账号资产详情：\n"#line:72
    O0OO0000O0000OOO0 +="\n当前杠杆账号风险率(默认3倍杠杆，小于2表示危险，需要人工处理): %s\n"%O0OO0O00OO0000OOO .get ("marginLevel")#line:73
    O0OO0000O0000OOO0 +="当前杠杆账号总资产估值: {0} BTC (约为 {1:.2f} USDT )\n".format (O0OO0O00OO0000OOO .get ("totalAssetOfBtc"),float (O0OO0O00OO0000OOO .get ("totalAssetOfBtc"))*OOOOOO0O00O0OOOOO )#line:74
    O0OO0000O0000OOO0 +="当前杠杆账号账户权益: {0} BTC (约为 {1:.2f} USDT )\n".format (O0OO0O00OO0000OOO .get ("totalNetAssetOfBtc"),float (O0OO0O00OO0000OOO .get ("totalNetAssetOfBtc"))*OOOOOO0O00O0OOOOO )#line:75
    O0OO0000O0000OOO0 +="当前帐户可用现金{0}是: {1}\n".format (usdt_symbol ,float (OOOO0O0OOO0O00OOO ))#line:77
    O0OO0000O0000OOO0 +="当前账户可用代币{0}是: {1}\n".format (coin_symbol ,float (OO0OO0OO00OOOOO0O ))#line:78
    print (O0OO0000O0000OOO0 )#line:79
    OOO0O0OOOO0O00OOO ="当前借入{}资产是{}\n".format (coin_symbol ,O00O0O00000O0OOO0 )#line:80
    OOO0O0OOOO0O00OOO +="当前{}的净资产是{}\n".format (coin_symbol ,O0O0000O00OOOO000 )#line:81
    print (OOO0O0OOOO0O00OOO )#line:82
def get_free_assets ():#line:85
    O000O000O00OO00O0 =client .get_margin_account ()#line:86
    O000OOOOOOOO000O0 =O000O000O00OO00O0 .get ('userAssets')#line:87
    print ("free cash: %.4f "%float (free_cash ))#line:89
    print ("free coin: %.4f "%float (free_coin ))#line:90
def get_margin_stream_keepalive (O0O0OO0O0OOO00O00 ):#line:92
    OOOOO00OO0O0000O0 =client .margin_stream_keepalive (O0O0OO0O0OOO00O00 )#line:93
    print (OOOOO00OO0O0000O0 )#line:94
def get_margin_listen_key ():#line:97
    OOO000000O000OOO0 =client .margin_stream_get_listen_key ()#line:98
    print (OOO000000O000OOO0 )#line:99
def retry_websocket ():#line:101
    OOOOOOO0OOOOO0O0O =BinanceSocketManager (client )#line:102
    OO0000OOOO00O0O0O =OOOOOOO0OOOOO0O0O .start_margin_socket (process_message )#line:103
    print ("websocket Conn key: "+OO0000OOOO00O0O0O )#line:104
    OOOOOOO0OOOOO0O0O .start ()#line:105
    time .sleep (1 )#line:106
    OOOOOOO0OOOOO0O0O .stop_socket (OO0000OOOO00O0O0O )#line:107
    OO0000OOOO00O0O0O =OOOOOOO0OOOOO0O0O .start_margin_socket (process_message )#line:108
    print ("renewer websocket Conn key: "+OO0000OOOO00O0O0O )#line:109
def process_message (O00O0OO00OO0O0O00 ):#line:111
    print (O00O0OO00OO0O0O00 )#line:112
def is_max_margins (O0O00O000O0O0O00O ):#line:114
    O0OOO0O000000O000 =client .get_open_margin_orders (symbol =symbol )#line:115
    if len (O0OOO0O000000O000 )>O0O00O000O0O0O00O :#line:116
        return True #line:117
    else :#line:118
        return False #line:119
def loan_asset (OO00OO000OO00O000 ,O0OOOOOOO0OOOOOOO ):#line:121
    OOOO0OOO0000O0O00 =client .get_margin_account ()#line:122
    O00O00OO00OOOOO0O =OOOO0OOO0000O0O00 .get ('userAssets')#line:123
    O0O0OO0000000000O =float (0 )#line:124
    for O0000000OO000OOO0 in O00O00OO00OOOOO0O :#line:125
        if O0000000OO000OOO0 .get ('asset')=='EOS':#line:126
            O0O0OO0000000000O =float (O0000000OO000OOO0 .get ('borrowed'))#line:127
    O0OOOOOOO0OOOOOOO =O0OOOOOOO0OOOOOOO -O0O0OO0000000000O #line:128
    if O0OOOOOOO0OOOOOOO <=float (0 ):#line:129
        print ('don\'t need loan, original loan: {}'.format (O0O0OO0000000000O ))#line:130
        pass #line:131
    else :#line:132
        OO00OO0O000000OO0 =client .create_margin_loan (asset =OO00OO000OO00O000 ,amount =O0OOOOOOO0OOOOOOO )#line:134
        print (OO00OO0O000000OO0 )#line:135
def repay_asset (O00O0O0OOOOO000OO ,O000OOO000O0O0OO0 ):#line:137
    O0OOOO0OOO0OO0OOO =client .repay_margin_loan (asset =O00O0O0OOOOO000OO ,amount =O000OOO000O0O0OO0 )#line:139
    print (O0OOOO0OOO0OO0OOO )#line:140
def get_all_margin_orders ():#line:142
    O0OO0000OO0000OOO =client .get_open_margin_orders (symbol =symbol )#line:143
    print (O0OO0000OO0000OOO )#line:144
def cacel_all_margin_orders ():#line:146
    O0OOOOO00O0OO0OOO =client .get_open_margin_orders (symbol =symbol )#line:147
    for OOO0000O0O00OO00O in O0OOOOO00O0OO0OOO :#line:148
        O0OO0O0OOOOOOO00O =client .cancel_margin_order (symbol =symbol ,orderId =OOO0000O0O00OO00O .get ('orderId'))#line:150
        print (O0OO0O0OOOOOOO00O )#line:151
def margin_account ():#line:153
    OO0000O000O0OO0O0 =client .get_margin_account ()#line:154
    OOOOO0OOO000O0OOO =OO0000O000O0OO0O0 .get ('userAssets')#line:155
    for O0O0O00O0O0OO0OOO in OOOOO0OOO000O0OOO :#line:156
        if O0O0O00O0O0OO0OOO .get ('asset')==coin_symbol :#line:157
            OOO0OOOO00O0O0000 =O0O0O00O0O0OO0OOO .get ('free')#line:158
        if O0O0O00O0O0OO0OOO .get ('asset')==usdt_symbol :#line:159
            OO0OOO000O0O000OO =O0O0O00O0O0OO0OOO .get ('free')#line:160
    print (OOO0OOOO00O0O0000 ,OO0OOO000O0O000OO )#line:162
def new_margin_order ():#line:164
    O0OOO000O00O0OO00 =client .get_orderbook_ticker (symbol =symbol )#line:165
    print ("Current bid price: {}".format (O0OOO000O00O0OO00 .get ('bidPrice')))#line:166
    print ("Current ask price: {}".format (O0OOO000O00O0OO00 .get ('askPrice')))#line:167
    O000OOO0OO0OOOO0O =float (O0OOO000O00O0OO00 .get ('bidPrice'))*float (1 -0.005 )#line:168
    O000OOO0OO0OOOO0O ='%.4f'%O000OOO0OO0OOOO0O #line:169
    O0000O0OOO0O00O0O =float (O0OOO000O00O0OO00 .get ('askPrice'))*float (1 +0.005 )#line:171
    O0000O0OOO0O00O0O ='%.4f'%O0000O0OOO0O00O0O #line:172
    OOO00O0OO00OO00OO =client .create_margin_order (symbol =symbol ,side =SIDE_BUY ,type =ORDER_TYPE_LIMIT ,quantity =10.0 ,price =O000OOO0OO0OOOO0O ,timeInForce =TIME_IN_FORCE_GTC )#line:179
    O00O0O0O00O00OO0O =client .create_margin_order (symbol =symbol ,side =SIDE_SELL ,type =ORDER_TYPE_LIMIT ,quantity =10.0 ,price =O0000O0OOO0O00O0O ,timeInForce =TIME_IN_FORCE_GTC )#line:186
if __name__ =="__main__":#line:188
    run ()