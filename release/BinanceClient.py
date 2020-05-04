from binance .client import Client #line:3
from binance .enums import *#line:4
from binance .websockets import BinanceSocketManager #line:5
import time #line:6
from BinanceKeys import BinanceKey1 #line:8
api_key =BinanceKey1 ['api_key']#line:10
api_secret =BinanceKey1 ['api_secret']#line:11
client =Client (api_key ,api_secret )#line:12
symbol ='EOSUSDT'#line:14
coin_symbol ='EOS'#line:15
usdt_symbol ='USDT'#line:16
max_margins =15 #line:17
def run ():#line:19
    print ('=========start running=================')#line:20
    print ("current orders")#line:22
    get_all_margin_orders ()#line:23
    print ('current free assets')#line:25
    get_free_assets ()#line:26
def get_free_assets ():#line:28
    OO0OO00000OOO0OO0 =client .get_margin_account ()#line:29
    O00OOO000O000OO00 =OO0OO00000OOO0OO0 .get ('userAssets')#line:30
    O0OO00OO00O00O0O0 =float (0 )#line:31
    OOOO0OOO00O000OO0 =float (0 )#line:32
    for O000000O00O000000 in O00OOO000O000OO00 :#line:33
        if O000000O00O000000 .get ('asset')==coin_symbol :#line:34
            O0OO00OO00O00O0O0 =O000000O00O000000 .get ('free')#line:35
        if O000000O00O000000 .get ('asset')==usdt_symbol :#line:36
            OOOO0OOO00O000OO0 =O000000O00O000000 .get ('free')#line:37
    print ("free cash: %.4f "%float (OOOO0OOO00O000OO0 ))#line:38
    print ("free coin: %.4f "%float (O0OO00OO00O00O0O0 ))#line:39
def get_margin_stream_keepalive (O00OO0O000000O00O ):#line:41
    OO0O0000OO000O000 =client .margin_stream_keepalive (O00OO0O000000O00O )#line:42
    print (OO0O0000OO000O000 )#line:43
def get_margin_listen_key ():#line:46
    OOO000OO0O000O0OO =client .margin_stream_get_listen_key ()#line:47
    print (OOO000OO0O000O0OO )#line:48
def retry_websocket ():#line:50
    O0OOO0O000OOOO00O =BinanceSocketManager (client )#line:51
    O0O00O00OOOO0000O =O0OOO0O000OOOO00O .start_margin_socket (process_message )#line:52
    print ("websocket Conn key: "+O0O00O00OOOO0000O )#line:53
    O0OOO0O000OOOO00O .start ()#line:54
    time .sleep (1 )#line:55
    O0OOO0O000OOOO00O .stop_socket (O0O00O00OOOO0000O )#line:56
    O0O00O00OOOO0000O =O0OOO0O000OOOO00O .start_margin_socket (process_message )#line:57
    print ("renewer websocket Conn key: "+O0O00O00OOOO0000O )#line:58
def process_message (OOOOO0O0O00O000O0 ):#line:60
    print (OOOOO0O0O00O000O0 )#line:61
def is_max_margins (O0OOOO0OO0OO00OO0 ):#line:63
    OO00O00O000OO0OO0 =client .get_open_margin_orders (symbol =symbol )#line:64
    if len (OO00O00O000OO0OO0 )>O0OOOO0OO0OO00OO0 :#line:65
        return True #line:66
    else :#line:67
        return False #line:68
def loan_asset (OOO000O0000O0O0O0 ,OO000OO0OOOOO00O0 ):#line:70
    OOOO0O0OO000O000O =client .get_margin_account ()#line:71
    O000O0O000O0OO0OO =OOOO0O0OO000O000O .get ('userAssets')#line:72
    OO00000O00O0000O0 =float (0 )#line:73
    for OOOO0OOO0OOOOOOO0 in O000O0O000O0OO0OO :#line:74
        if OOOO0OOO0OOOOOOO0 .get ('asset')=='EOS':#line:75
            OO00000O00O0000O0 =float (OOOO0OOO0OOOOOOO0 .get ('borrowed'))#line:76
    OO000OO0OOOOO00O0 =OO000OO0OOOOO00O0 -OO00000O00O0000O0 #line:77
    if OO000OO0OOOOO00O0 <=float (0 ):#line:78
        print ('don\'t need loan, original loan: {}'.format (OO00000O00O0000O0 ))#line:79
        pass #line:80
    else :#line:81
        O00O00O000OOO0OO0 =client .create_margin_loan (asset =OOO000O0000O0O0O0 ,amount =OO000OO0OOOOO00O0 )#line:83
        print (O00O00O000OOO0OO0 )#line:84
def repay_asset (OOOO000OOO0O0000O ,OOOO000OOOO0000O0 ):#line:86
    OO0OOOO00OOOOOO00 =client .repay_margin_loan (asset =OOOO000OOO0O0000O ,amount =OOOO000OOOO0000O0 )#line:88
    print (OO0OOOO00OOOOOO00 )#line:89
def get_all_margin_orders ():#line:91
    O0O0OOO0O0OO000O0 =client .get_open_margin_orders (symbol =symbol )#line:92
    print (O0O0OOO0O0OO000O0 )#line:93
def cacel_all_margin_orders ():#line:95
    OOOO00OO0000O0OO0 =client .get_open_margin_orders (symbol =symbol )#line:96
    for OO0000OOO0OOO00OO in OOOO00OO0000O0OO0 :#line:97
        O000OOOO0O0000O0O =client .cancel_margin_order (symbol =symbol ,orderId =OO0000OOO0OOO00OO .get ('orderId'))#line:99
        print (O000OOOO0O0000O0O )#line:100
def margin_account ():#line:102
    OOO0OO0OOO000OOOO =client .get_margin_account ()#line:103
    OOO00O0000O00OOOO =OOO0OO0OOO000OOOO .get ('userAssets')#line:104
    for OOO0O00O00OOOO0O0 in OOO00O0000O00OOOO :#line:105
        if OOO0O00O00OOOO0O0 .get ('asset')==coin_symbol :#line:106
            OO0O00OO00000OO0O =OOO0O00O00OOOO0O0 .get ('free')#line:107
        if OOO0O00O00OOOO0O0 .get ('asset')==usdt_symbol :#line:108
            O00OOO0000OOOO0O0 =OOO0O00O00OOOO0O0 .get ('free')#line:109
    print (OO0O00OO00000OO0O ,O00OOO0000OOOO0O0 )#line:111
def new_margin_order ():#line:113
    OO0O0OO0OOO0OO00O =client .get_orderbook_ticker (symbol =symbol )#line:114
    print ("Current bid price: {}".format (OO0O0OO0OOO0OO00O .get ('bidPrice')))#line:115
    print ("Current ask price: {}".format (OO0O0OO0OOO0OO00O .get ('askPrice')))#line:116
    OO00OO0000OO0O000 =float (OO0O0OO0OOO0OO00O .get ('bidPrice'))*float (1 -0.005 )#line:117
    OO00OO0000OO0O000 ='%.4f'%OO00OO0000OO0O000 #line:118
    OOOO0000O0O0OO0O0 =float (OO0O0OO0OOO0OO00O .get ('askPrice'))*float (1 +0.005 )#line:120
    OOOO0000O0O0OO0O0 ='%.4f'%OOOO0000O0O0OO0O0 #line:121
    OOO00OO0O000000OO =client .create_margin_order (symbol =symbol ,side =SIDE_BUY ,type =ORDER_TYPE_LIMIT ,quantity =10.0 ,price =OO00OO0000OO0O000 ,timeInForce =TIME_IN_FORCE_GTC )#line:128
    O0OOO0O00OO000000 =client .create_margin_order (symbol =symbol ,side =SIDE_SELL ,type =ORDER_TYPE_LIMIT ,quantity =10.0 ,price =OOOO0000O0O0OO0O0 ,timeInForce =TIME_IN_FORCE_GTC )#line:135
if __name__ =="__main__":#line:137
    run ()