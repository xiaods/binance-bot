#!/bin/sh

echo "start strading bot"
echo "====================="

python3 binance_bot.py > bot.log 2>&1 &

echo "Done!"