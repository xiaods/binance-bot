#!/bin/sh


echo Qcat Automate Trading Bot Release Script
echo "=========================================="

echo copy release files to release folder

cp BinanceBot.py BinanceTop.py BinanceKeys.py ProfitReport.py rebuy_coin.py resell_coin.py settings.py ./release/

latesttag=$(git describe --tags)
echo release qcat version: ${latesttag}

zip -q -r -e -o "qcat-release-${latesttag}.zip" ./release
echo "Done!"