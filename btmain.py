# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pyfolio as pf
import datetime as dt
import pandas_datareader.data as web
import requests

# print all outputs
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

def RSI(data, days, adjust=False):
    delta = data['Close'].diff(1).dropna()
    price_fall = delta.copy()
    price_raise = delta.copy()

    price_raise[price_raise < 0] = 0
    price_fall[price_fall > 0] = 0

    pirce_raise_ewm = price_raise.ewm(com=days - 1, adjust=adjust).mean()
    price_fall_ewm = abs(price_fall.ewm(com=days - 1, adjust=adjust).mean())

    RSI = 100 - 100 / (1 + pirce_raise_ewm / price_fall_ewm)

    return RSI



# downloading historical necessary data for backtesting and analysis
_end_ = dt.date.today()
year = dt.datetime.now().year
_start_ = dt.date(year - 10,1,2)
ticker = input("The tick you want to backtest: ")
df = yf.download(ticker, start = _start_, end = _end_)

# calculating rate of price spread
df['rate of price spread'] = round((((df['Close'] - df['Close'].shift(1)) / df['Close'].shift(1))) * 100, 2)

# calculating RSI
df['RSI'] = RSI(df, 14)


print(*df)
print(df.tail(5).sort_index(ascending = False))