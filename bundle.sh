#!/bin/sh


echo Qcat Automate Trading Bot Release Script
echo "=========================================="

rm -rf release && mkdir release

echo "copy core bot file to release..."
cp  -avr binance_bot.py binance_top.py binance_orders.py binance_report.py \
    settings_tpl.py requirements.txt ./release/

echo "some useful scripts for trading..."
cp  -avr ./utility ./release/

echo "some bash script to get thing start..."
cp -avr ./scripts/*.sh ./release/

echo "Now starting bundle the code and package it..."

git fetch origin master  --tags

latesttag=$(git describe --tags)
echo checking out ${latesttag}
git checkout ${latesttag}

zip -q -r -e -o "qcat-release-${latesttag}.zip" ./release
echo "Done!"