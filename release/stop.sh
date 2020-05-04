#!/bin/sh

echo stop trading bot

kill -9 $( ps aux|grep BinanceBot.py|grep -v grep|awk '{print $2}' )

