## Automate trading bot for binance

### install python-binance client

```bash
apt-get update
apt-get install python3-pip
pip3 install python-binance
```

### Update your binance api keys

update BinanceKeys.py  api_key

### Run BinanceBot.py

start.sh


### How do I protect my Python source code?

```
pip install sourcedefender

$ cat /home/ubuntu/helloworld.py
print("Hello World!")

$ sourcedefender encrypt --ttl=1d /home/ubuntu/helloworld.py
SOURCEdefender v5.0.12

Processing:

/home/ubuntu/helloworld.py

$ cat /home/ubuntu/helloworld.pye
-----BEGIN SOURCEDEFENDER FILE-----
Version : 5.0.12

KkVjZjNWRV4rZvmUFhXBQhPwlR6wUWASZO/Gnh8sJKzpW7c3D8TRbLfNXn01Q182QigxeW1tagq1
c8A0WiWh5wa2k7YCd4oNugSqv/FABal7Wh1vDsVh7rPXFcamQhfqU1kv5CtmN/2G1EqRUy2PGu+p
camVzPjFXmFkQ21+fj80MUg0Z1oG3PniOXCJ0V/Qu3/Bw0Fic0BZTGxjTm4=

------END SOURCEDEFENDER FILE------

$ python3 -m sourcedefender /home/ubuntu/helloworld.pye
Hello World!
$

$ cd /home/ubuntu
$ ls
helloworld.pye
$ python3
>>>
>>> import sourcedefender
>>> import helloworld
Hello World!
>>> exit()
$
```




