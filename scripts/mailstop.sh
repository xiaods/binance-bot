#!/bin/sh

echo "stop mail cronjob"
echo "===================="

kill -9 $( ps aux|grep ProfitReport.py|grep -v grep|awk '{print $2}' )
