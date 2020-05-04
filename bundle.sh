#!/bin/sh


echo Qcat Automate Trading Bot Release Script
echo "=========================================="


git fetch origin master  --tags

latesttag=$(git describe --tags)
echo checking out ${latesttag}
git checkout ${latesttag}

zip -q -r -e -o "qcat-release-${latesttag}.zip" ./release
echo "Done!"