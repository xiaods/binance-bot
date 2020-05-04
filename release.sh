#!/bin/sh


echo Qcat Automate Trading Bot Release Script
echo "=========================================="

latesttag=$(git describe --tags)
echo release qcat version: ${latesttag}

zip -q -r -e -o "qcat-release-${latesttag}.zip" ./release
echo "Done!"