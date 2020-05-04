""#line:7
import time #line:8
from datetime import datetime #line:9
import sys #line:10
import signal #line:11
from binance .client import Client #line:13
from binance .enums import *#line:14
from binance .websockets import BinanceSocketManager #line:15
from twisted .internet import reactor #line:16
from BinanceKeys import BinanceKey1 #line:18
API_KEY =BinanceKey1 ['api_key']#line:19
API_SECRET =BinanceKey1 ['api_secret']#line:20
client =Client (API_KEY ,API_SECRET )#line:21
symbol ='EOSUSDT'#line:24
eos_symbol ='EOS'#line:25
usdt_symbol ='USDT'#line:26
loan =200 #line:27
depth =10 #line:28
qty =loan /depth #line:29
max_margins =(depth *2 )*(0.6 )#line:30
def run ():#line:32
    initialize_arb ()#line:33
def initialize_arb ():#line:35
    OOOOO0O0OOOOO00O0 ="\n\n---------------------------------------------------------\n\n"#line:36
    OOOOO0O0OOOOO00O0 +="Binance auto trading bot\n"#line:37
    OOOO0O000OO0O00OO =str (datetime .now ())#line:38
    OOOOO0O0OOOOO00O0 +="\nBot Start Time: {}\n\n\n".format (OOOO0O000OO0O00OO )#line:39
    print (OOOOO0O0OOOOO00O0 )#line:40
    data_log_to_file (OOOOO0O0OOOOO00O0 )#line:41
    time .sleep (1 )#line:42
    OO00O0O0OOO0O0000 =client .get_system_status ()#line:43
    print ("\nExchange Status: ",OO00O0O0OOO0O0000 )#line:44
    cancel_all_margin_orders (symbol )#line:48
    loan_asset (eos_symbol ,loan )#line:50
    new_margin_order (symbol ,qty )#line:52
    global bm ,conn_key #line:55
    bm =BinanceSocketManager (client )#line:56
    conn_key =bm .start_margin_socket (process_message )#line:57
    print ("websocket Conn key: "+conn_key )#line:58
    bm .start ()#line:59
    while True :#line:62
        get_margin_stream_keepalive (conn_key )#line:63
        time .sleep (60 *30 )#line:64
def new_margin_order (O00OOO0OOOO0OO000 ,O0OO0OOO00O000O0O ):#line:66
    OOOO00O00O00000O0 =client .get_orderbook_ticker (symbol =O00OOO0OOOO0OO000 )#line:69
    print ("Current bid price: {}".format (OOOO00O00O00000O0 .get ('bidPrice')))#line:70
    print ("Current ask price: {}".format (OOOO00O00O00000O0 .get ('askPrice')))#line:71
    O000OOOO0O0OO00O0 =float (OOOO00O00O00000O0 .get ('bidPrice'))*float (1 -0.005 )#line:72
    O000OOOO0O0OO00O0 ='%.4f'%O000OOOO0O0OO00O0 #line:73
    OO0O0OOOO0OOO00O0 =float (OOOO00O00O00000O0 .get ('askPrice'))*float (1 +0.005 )#line:75
    OO0O0OOOO0OOO00O0 ='%.4f'%OO0O0OOOO0OOO00O0 #line:76
    OO0O0OOO00OOO000O =client .get_margin_account ()#line:79
    O0OO0000O00OOOO0O =OO0O0OOO00OOO000O .get ('userAssets')#line:80
    O0O000OO0OO00O0O0 =float (0 )#line:81
    for OOO0O0O0OO0OOOOOO in O0OO0000O00OOOO0O :#line:82
        if OOO0O0O0OO0OOOOOO .get ('asset')==eos_symbol :#line:83
            O0O000OO0OO00O0O0 =float (OOO0O0O0OO0OOOOOO .get ('free'))#line:84
    if O0O000OO0OO00O0O0 <loan *float (0.3 ):#line:86
        print ("Current Account coin balance is less then 30%. don't do order anymore.")#line:87
        return #line:88
    OOO00000OOO00OO0O =client .create_margin_order (symbol =O00OOO0OOOO0OO000 ,side =SIDE_BUY ,type =ORDER_TYPE_LIMIT ,quantity =O0OO0OOO00O000O0O ,price =O000OOOO0O0OO00O0 ,timeInForce =TIME_IN_FORCE_GTC )#line:95
    OO0O000OO0OO0OOOO =client .create_margin_order (symbol =O00OOO0OOOO0OO000 ,side =SIDE_SELL ,type =ORDER_TYPE_LIMIT ,quantity =O0OO0OOO00O000O0O ,price =OO0O0OOOO0OOO00O0 ,timeInForce =TIME_IN_FORCE_GTC )#line:102
def cancel_all_margin_orders (O000O0O00OOO0O0O0 ):#line:104
    O00OOOO000OO000O0 =client .get_open_margin_orders (symbol =O000O0O00OOO0O0O0 )#line:105
    for OO000O00OOO0O0O00 in O00OOOO000OO000O0 :#line:106
        OOOO000O0OOOO0O0O =client .cancel_margin_order (symbol =O000O0O00OOO0O0O0 ,orderId =OO000O00OOO0O0O00 .get ('orderId'))#line:108
        print (OOOO000O0OOOO0O0O )#line:109
'''
purpose: 杠杆交易怕平仓，所以通过最简化的交易单数可以判断出是否超出仓位

'''#line:114
def is_max_margins (OO0OO00O000O0OO00 ):#line:115
    OOOOOO0000O00O0O0 =client .get_open_margin_orders (symbol =symbol )#line:116
    if len (OOOOOO0000O00O0O0 )>OO0OO00O000O0OO00 :#line:117
        return True #line:118
    else :#line:119
        return False #line:120
'''
purpose: 自动借币

if account.loan 有币:
    pass
'''#line:127
def loan_asset (OOOOOO0OO0O0O000O ,OOO0000000OO00OOO ):#line:128
    O000O0OO0O0OO0O0O =client .get_margin_account ()#line:129
    O00O0OO00O0OO0OO0 =O000O0OO0O0OO0O0O .get ('userAssets')#line:130
    OO00OOO0OOO0OO0OO =float (0 )#line:131
    for OOO0O0OOOOOO0OOOO in O00O0OO00O0OO0OO0 :#line:132
        if OOO0O0OOOOOO0OOOO .get ('asset')=='EOS':#line:133
            OO00OOO0OOO0OO0OO =float (OOO0O0OOOOOO0OOOO .get ('borrowed'))#line:134
    OOO0000000OO00OOO =OOO0000000OO00OOO -OO00OOO0OOO0OO0OO #line:135
    if OOO0000000OO00OOO <=float (0 ):#line:136
        print ('don\'t need loan, original loan: {}'.format (OO00OOO0OOO0OO0OO ))#line:137
        pass #line:138
    else :#line:139
        O0O000000O0O0OOO0 =client .create_margin_loan (asset =OOOOOO0OO0O0O000O ,amount =OOO0000000OO00OOO )#line:141
        print (O0O000000O0O0OOO0 )#line:142
def process_message (OO00000O0OOO00OO0 ):#line:144
    if OO00000O0OOO00OO0 ['e']=='error':#line:145
        OO000000OOO00OO0O ="\n\n---------------------------------------------------------\n\n"#line:146
        OO000000OOO00OO0O +="websocket error:\n"#line:147
        OO000000OOO00OO0O +=OO00000O0OOO00OO0 .get ('m')#line:148
        print (OO000000OOO00OO0O )#line:149
        bm .stop_socket (O0OOO00OO0O00OOO0 )#line:151
        O0OOO00OO0O00OOO0 =bm .start_margin_socket (process_message )#line:152
        print ("renewer websocket Conn key: "+O0OOO00OO0O00OOO0 )#line:153
    else :#line:154
        if is_max_margins (max_margins )==True :#line:157
            print ("Come across max margins limits....return, don't do order anymore.")#line:158
            return #line:159
        if OO00000O0OOO00OO0 .get ('e')=='executionReport'and OO00000O0OOO00OO0 .get ('s')==symbol :#line:162
            print (OO00000O0OOO00OO0 )#line:163
        if OO00000O0OOO00OO0 .get ('e')=='executionReport'and OO00000O0OOO00OO0 .get ('s')==symbol and OO00000O0OOO00OO0 .get ('X')==ORDER_STATUS_FILLED :#line:165
            new_margin_order (symbol ,qty )#line:166
'''
Purpose: Keepalive a user data stream to prevent a time out. 
User data streams will close after 60 minutes. 
It's recommended to send a ping about every 30 minutes.
'''#line:172
def get_margin_stream_keepalive (OO00000OOO000O0OO ):#line:173
    OO000OO0O0O00O0OO =client .margin_stream_keepalive (OO00000OOO000O0OO )#line:174
    return OO000OO0O0O00O0OO #line:175
def term_sig_handler (O000OO00OO0000O0O ,OOOOO00OO0OOO0000 ):#line:177
    print ('catched singal: %d'%O000OO00OO0000O0O )#line:178
    reactor .stop ()#line:179
    sys .exit ()#line:180
def data_log_to_file (O00OOO000OO00OO0O ):#line:182
    with open ('CryptoBot_DataLog.txt','a+')as OO0OO0OOO0O0O00OO :#line:183
        OO0OO0OOO0O0O00OO .write (O00OOO000OO00OO0O )#line:184
if __name__ =="__main__":#line:186
    signal .signal (signal .SIGTERM ,term_sig_handler )#line:187
    signal .signal (signal .SIGINT ,term_sig_handler )#line:188
    signal .signal (signal .SIGHUP ,term_sig_handler )#line:189
    run ()