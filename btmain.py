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


# 下載10年間的股票數據
_end_ = dt.date.today()
year = dt.datetime.now().year
_start_ = dt.date(year - 10,1,2)
ticker = input("The tick you want to backtest: ")
df = yf.download(ticker, start = _start_, end = _end_)

# 計算單日漲跌幅
df['Rate of Price Spread'] = Rate_of_Price_Spread(df)

# 計算RSI
df['RSI'] = RSI(df, 14)


print(*df)
print(df.tail(5).sort_index(ascending = False))