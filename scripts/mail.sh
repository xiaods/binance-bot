#!/bin/sh

echo "start profit report cronjob every 12"
echo "======================================="

python3 ProfitReport.py > mail.log 2>&1 &
