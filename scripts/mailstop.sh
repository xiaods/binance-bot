#!/bin/sh

echo "stop mail cronjob"
echo "===================="

kill -9 $( ps aux|grep binance_report.py|grep -v grep|awk '{print $2}' )


echo "Done!"
