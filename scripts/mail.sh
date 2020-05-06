#!/bin/sh

echo "start profit report cronjob every 12"
echo "======================================="

python3 binance_report.py > mail.log 2>&1 &


echo "Done!"
