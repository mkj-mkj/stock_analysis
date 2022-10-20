# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pyfolio as pf
import datetime as dt
import pandas_datareader.data as web
import requests
from indicator import *
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
plt.switch_backend('agg')
# 下載10年間的股票數據
#symbols = input("The tick you want to backtest: ")
symbols = 'TSLA'    
ticker = yf.Ticker(symbols)
df = ticker.history(period='10y', interval='1d')
Aroon(df, 14)
print(*df)
print(df.tail(5).sort_index(ascending = False))

df.to_excel(R'Result.xlsx', sheet_name='Result')