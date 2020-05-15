# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
from settings import ZohoMail

from settings import MarginAccount
from settings import BinanceKey1
api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']
client = Client(api_key, api_secret, {"verify": True, "timeout": 10000})

# 配置参数
pair_symbol = MarginAccount['pair_symbol']
coin_symbol = MarginAccount['coin_symbol']
usdt_symbol = MarginAccount['usdt_symbol']
bnb_symbol = MarginAccount['bnb_symbol']
max_margins = 15
# 投入本金，手工统计
base_balance = MarginAccount['base_balance']
fiat_symbol = MarginAccount['fiat_symbol']
fiat_price = MarginAccount['fiat_price']
base_bnb_balance = MarginAccount['base_bnb_balance']

def eSend(sender,recipient,username,password,smtpserver,port, subject,e_content):
  try:
    #邮件头
    message = MIMEMultipart()
    message['From'] = sender #发送
    message['To'] = ",".join(recipient) #收件
    message['Subject'] = Header(subject, 'utf-8')
    message.attach(MIMEText(e_content, 'plain', 'utf-8')) # 邮件正文

    #执行
    server = smtplib.SMTP_SSL(smtpserver, port)
    server.login(username, password)
    server.sendmail(sender, recipient, message.as_string()) #发送
    server.quit()
    print("SEND")
  except Exception as e:
    print(e)
    print("SEND FAILED")

def run():
    while True:
        #配置
        #__time_____
        ehour=11 #定时小时
        emin=49 #定时分钟
        esec=50 #定时秒
        current_time = time.localtime(time.time())   #当前时间date
        cur_time = time.strftime('%H:%M', time.localtime(time.time()))       #当前时间str

        #__email_____
        sender = 'support@qcat.io' # 发件人邮箱
        recipient = ZohoMail['recipient'] # 收件人邮箱，可以多个（列表形式）群发
        username = ZohoMail['username'] # 发件人姓名
        password = ZohoMail['password'] # smtp密码，qq是给你分配一串，163是自己设置
        smtpserver = ZohoMail['smtpserver'] # 邮箱服务器
        serverport  = ZohoMail['serverport']

        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d")
        subject = "QCat Auto Trading Bot Report - {}".format(dt_string)  #邮件标题
        e_content = '{0:^27}\n{1:^27}\n{2:^25}\n{3:^25}'.format('i','/  \\','(-----)','(--------)')  #邮件正文
        e_content += "今天行情不错奥，Qcat自动交易机器人帮您统计了一下收益：\n\n"
        e_content += get_account_status()
        
        #操作
        if ((current_time.tm_hour == ehour) and (current_time.tm_min == emin) and (current_time.tm_sec == esec)):
            print ("START")
            eSend(sender, recipient, username, password, smtpserver, serverport, subject, e_content)
            print(cur_time)
        # sleep 1 second
        time.sleep(1)


def get_account_status():
    coinusdt_avg_price = client.get_avg_price(symbol=pair_symbol)
    bnbusdt_avg_price = client.get_avg_price(symbol='BNBUSDT')
    btcusdt_avg_price = client.get_avg_price(symbol='BTCUSDT')
    current_coin_price = float(coinusdt_avg_price.get('price'))
    current_bnb_price = float(bnbusdt_avg_price.get('price'))
    current_btc_price = float(btcusdt_avg_price.get('price'))
    message = "QCat Auto Trading bot\n"
    message += "-"*30 
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    message += "\n统计时间：%s\n" % dt_string
    message += "当前 {} 价格: {:.2f} USDT\n".format(coin_symbol, current_coin_price)
    message += "当前 BTC 价格: {:.2f} USDT\n".format(current_btc_price)
    message += "当前 BNB 价格: {:.2f} USDT\n\n".format(current_bnb_price)

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
    message += "当前账户可用{0}是: {1}\n".format(bnb_symbol, float(bnb_free_coin) )
    message += "-"*30
    message += "\n当前借入{}资产是{}\n".format(coin_symbol, loan_coin)
    message += "当前{}的净资产是{}\n".format(coin_symbol, net_coin)
    return message

if __name__ == "__main__":
    run()
