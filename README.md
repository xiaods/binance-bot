## QCat Automated Crypto Trading bot

### 对于小于4G内存的小机器，增加Swap
please install ta-lib component

RAM > 1G or add swap

```bash
# (增加4G)
dd if=/dev/zero of=/tmp/mem.swap bs=1M count=4096
free -m

mkswap /tmp/mem.swap
swapon /tmp/mem.swap
# 确认是否增加成功：
free -m
```

### 安装RSI指标计算库依赖
```bash
apt-get upgrade
apt-get install build-essential

# download from 
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz

tar -xvf ta-lib-0.4.0-src.tar.gz

cd ta-lib

./configure --prefix=/usr

make && make install

apt-get install python3-pip
### rsi指标
pip3 install numpy -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip3 install ta-lib

pip3 install pandas -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip3 install -r requirements.txt
```

### 安装并配置
bash setup.sh #初始化安装
settings.py   #bot全局配置，运行前务必配置

### 打包发行安装包
bash bundle.sh 生成安装包并发行zip格式包

start.sh  启动机器人
stop.sh  暂停机器人
top.sh  查询当前账户挂单状态
mail.sh  发盈利报告邮件，12小时统计发送一次
mailstop.sh  停止邮件

### How do I protect my Python source code?

在线混淆工具：http://pyob.oxyry.com/

选择：Dancing Links

专业工具(only Linux)：https://github.com/Hnfull/Intensio-Obfuscator

