#!/bin/sh


echo Qcat Automate Trading Bot Release Script
echo "=========================================="

echo copy release files to release folder

cp  BinanceBot.py BinanceTop.py BinanceKeys.py \
    ProfitReport.py rebuy_coin.py resell_coin.py \
    rebuy_bnb.py \
    settings.py BinanceOrders.py ./release/

cp ./scripts/*.sh ./release/

echo "Done!"