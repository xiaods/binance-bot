#!/bin/sh

echo "stop trading bot"
echo "===================="

# 停止机器人
kill -9 $( ps aux|grep BinanceBot.py|grep -v grep|awk '{print $2}' )
