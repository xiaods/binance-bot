#!/bin/sh

echo "stop trading bot"
echo "===================="

# 停止机器人
kill -9 $( ps aux|grep bnb_stochrsi_bot.py|grep -v grep|awk '{print $2}' )

echo "Done!"