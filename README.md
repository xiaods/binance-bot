## QCat Automated Crypto Trading bot

### 更新依赖库
```bash
apt-get update
apt install python3-pip
pip3 install -r requirements.txt
```
### 安装并配置
bash setup.sh #初始化安装
settings.py   #bot全局配置，运行前务必配置

### 打包安装
bash copyfile.sh 复制文件
bash bundle.sh 生成安装包

start.sh  启动机器人
stop.sh  暂停机器人
top.sh  查询当前账户挂单状态
mail.sh  发盈利报告邮件，12小时统计发送一次
mailstop.sh  停止邮件

### How do I protect my Python source code?

在线混淆工具：http://pyob.oxyry.com/

选择：Dancing Links

专业工具(only Linux)：https://github.com/Hnfull/Intensio-Obfuscator

