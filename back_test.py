import pandas as pd
import numpy as np
import yfinance as yf
import pyfolio as pf
import datetime as dt
import pandas_datareader.data as web
import requests
from strategy import *
from indicator import *
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

money = 10000

symbols = 'AAPL'    
ticker = yf.Ticker(symbols)
df = ticker.history(period='10y', interval='1d')

RSI(df, 14)
hold = 0
df['Buy&Sell'] = ""
df['Hold'] = ""
for i in range(3, len(df)):
    #RSI連續3天小於50且連續上升3天, 則買入
    if (((df['RSI'])[i] < 50) and (df['RSI'])[i-1] < 50) and ((df['RSI'])[i-2] < 50) and (((df['RSI'])[i] > (df['RSI'])[i-1]) and (((df['RSI'])[i] > (df['RSI'])[i-1]))):
        (df['Buy&Sell'])[i] = 'Buy'
        if money > 10 * (df['Open'])[i]: #一次買入10股
            hold += 10
            money -= 10 * (df['Open'])[i]
        (df['Hold'])[i] = 'Buy in'
    #RSI連續3天大於50且連續下降3天, 則賣出
    elif (((df['RSI'])[i] > 50) and (df['RSI'])[i-1] > 50) and ((df['RSI'])[i-2] > 50) and (((df['RSI'])[i] < (df['RSI'])[i-1]) and (((df['RSI'])[i] < (df['RSI'])[i-1]))):
        (df['Buy&Sell'])[i] = 'Sell'

        if hold >= 10: #持股數超過10股時, 則一次賣出10股
            hold -= 10
            money += 10 * (df['Open'])[i]
            (df['Hold'])[i] = 'Sold out'

print(hold)
print(money)
print(hold * df['Close'][-1] + money) #資產總額
print("Benefit = {:.2f}%".format((hold * df['Close'][-1] + money - 10000) / 100))


df.to_excel(R'BackTest.xlsx', sheet_name='Result')