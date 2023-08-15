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

symbols = 'MRNA'    
ticker = yf.Ticker(symbols)
df = ticker.history(period='10y', interval='1d')

strategy_beta(df) #使用beta版策略

hold = 0
df['Hold'] = 0
df['NumOfStuck'] = ''
for i in range(0, len(df)):
    if (df['Buy&Sell'])[i] == 'Buy' and money > 10 * (df['Open'])[i]: #如果適合買入且有餘額, 一次買入10股 
        hold += 10
        money -= 10 * (df['Open'])[i]
        (df['Hold'])[i] = 'Buy in' #狀態更新
    elif (df['Buy&Sell'])[i] == 'Sell' and hold >= 10: #如果適合賣出且有剩餘持股, 一次賣出10股 
        hold -= 10
        money += 10 * (df['Open'])[i]
        (df['Hold'])[i] = 'Sold out' #狀態更新

    df['NumOfStuck'][i] = hold

print(hold)
print(money)
print(hold * df['Close'][-1] + money) #資產總額
print("Benefit = {:.2f}%".format((hold * df['Close'][-1] + money - 10000) / 100))


df.to_excel(R'BackTest.xlsx', sheet_name='Result')