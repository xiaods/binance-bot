#!/bin/sh


echo Qcat Automate Trading Bot Release Script
echo "=========================================="

rm -rf release && mkdir release

echo "copy core bot file to release..."
cp  binance_bot.py binance_top.py binance_orders.py binance_report.py \
    settings.py ./release/

echo "some useful scripts for trading..."
cp  rebuy_bnb.py rebuy_coin.py repay_margin_loan.py \
    resell_coin.py ./release/

echo "some bash script to get thing start..."
cp ./scripts/*.sh ./release/

echo "Done!"