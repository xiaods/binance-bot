# coding: utf-8
import pandas as pd
import talib
import numpy as np #computing multidimensionla arrays
import datetime
import time
from settings import BinanceKey1


# Initialize Client and connect to Binance
from binance.client import Client
api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']
client = Client(api_key, api_secret, {"verify": True, "timeout": 10000})

# StochasticRSI Function
def Stoch(close,high,low, smoothk, smoothd, n):
    lowestlow = pd.Series.rolling(low,window=n,center=False).min()
    highesthigh = pd.Series.rolling(high, window=n, center=False).max()
    K = pd.Series.rolling(100*((close-lowestlow)/(highesthigh-lowestlow)), window=smoothk).mean()
    D = pd.Series.rolling(K, window=smoothd).mean()
    return K, D

#################################### Logging #################################################
print("Date                    Close         RSI           %K             %D")
##############################################################################################

# Main program
while True:
    # ping client to avoid timeout
    client = Client(api_key, api_secret)

    # Get Binance Data into dataframe
    candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE)
    df = pd.DataFrame(candles)
    df.columns=['timestart','open','high','low','close','?','timeend','?','?','?','?','?']
    df.timestart = [datetime.datetime.fromtimestamp(i/1000) for i in df.timestart.values]
    df.timeend = [datetime.datetime.fromtimestamp(i/1000) for i in df.timeend.values]

    # Compute RSI after fixing data
    float_data = [float(x) for x in df.close.values]
    np_float_data = np.array(float_data)
    rsi = talib.RSI(np_float_data, 14)
    df['rsi'] = rsi

    # Compute StochRSI using RSI values in Stochastic function
    mystochrsi = Stoch(df.rsi, df.rsi, df.rsi, 3, 3, 14)
    df['MyStochrsiK'],df['MyStochrsiD'] = mystochrsi

#################################### End of Main #############################################
# WARNING: If Logging is removed uncomment the next line.
    time.sleep(1) # Sleep for 1 second. So IP is not rate limited. Can be faster. Up to 1200 requests per minute.

#################################### Logging #################################################
    newestcandlestart = df.timestart.astype(str).iloc[-1] #gets last time
    newestcandleend = df.timeend.astype(str).iloc[-1] #gets current time?
    newestcandleclose = df.close.iloc[-1] #gets last close
    newestcandleRSI = df.rsi.astype(str).iloc[-1] #gets last rsi
    newestcandleK = df.MyStochrsiK.astype(str).iloc[-1] #gets last rsi
    newestcandleD = df.MyStochrsiD.astype(str).iloc[-1] #gets last rsi

    print(newestcandleend + " " +newestcandleclose + " "
                    + newestcandleRSI + " "
                    + newestcandleK + " "
                    + newestcandleD )
    #Sleeps every 29 seconds and wakes up to post to logger.
    # t = datetime.datetime.utcnow()
    # sleeptime = (t.second)
    # if sleeptime == 0 or sleeptime ==30:
    #     logger.info(newestcandleclose + " "
    #                 + newestcandleRSI + " "
    #                 + newestcandleK + " "
    #                 + newestcandleD )
    # time.sleep(1)
##############################################################################################