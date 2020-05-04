## Automate trading bot for binance

### install python-binance client

```bash
apt-get update
apt-get install python3-pip
pip3 install python-binance
```

### Update your binance api keys

update BinanceKeys.py  api_key

### 部署安装Bot

直接复制release目录下程序到主机上即可：

start.sh  启动机器人
stop.sh  暂停机器人
top.sh  查询当前账户挂单状态


### How do I protect my Python source code?

在线混淆工具：http://pyob.oxyry.com/

选择：Dancing Links

专业工具：https://github.com/Hnfull/Intensio-Obfuscator


### 发布安装包

zip -q -r -e -o qcat-release.zip ./release 



