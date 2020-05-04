## QCat Automated Crypto Trading bot

### 更新依赖库
```bash
apt-get update
apt-get install python3-pip
pip3 install python-binance
```

### 更新配置

BinanceKeys.py： 币安交易所key/ secret
settings.py: 邮件服务器配置

### 部署安装Bot

bash bundle.sh 生成安装包

start.sh  启动机器人
stop.sh  暂停机器人
top.sh  查询当前账户挂单状态
mail.sh  发盈利报告邮件，12小时统计发送一次
mailstop.sh  停止邮件


### How do I protect my Python source code?

在线混淆工具：http://pyob.oxyry.com/

选择：Dancing Links

专业工具：https://github.com/Hnfull/Intensio-Obfuscator


### 发布安装包步骤

1. bash copyfile.sh
2. bash bundle.sh



