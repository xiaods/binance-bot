#!/bin/sh

echo profit report cronjob
echo ======================

python3 ProfitReport.py > mail.log 2>&1 &
