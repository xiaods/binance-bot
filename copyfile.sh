#!/bin/sh


echo Qcat Automate Trading Bot Release Script
echo "=========================================="

rm -rf release && mkdir release

echo "copy core bot file to release..."
cp  binance_bot.py binance_top.py binance_orders.py binance_report.py \
    settings_tpl.py ./release/

echo "some useful scripts for trading..."
cp  -avr ./utility ./release/

echo "some bash script to get thing start..."
cp ./scripts/*.sh ./release/

echo "Done!"