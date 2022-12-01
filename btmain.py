# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pyfolio as pf
import datetime as dt
import pandas_datareader.data as web
from indicator import *
from strategy import * 
from sp500_read import *
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
plt.switch_backend('agg')
# 下載10年間的股票數據
#symbols = input("The tick you want to backtest: ")
period_test = input("Input the period(d, mo, y): ")


symbols_list = read_sp500()
buy = []
sell = []
hold = []

for i in symbols_list:
    B_S = 0
    ticker = yf.Ticker(i)
    df = ticker.history(period= period_test, interval='1d')
    B_S = strategy_beta(df)
    if B_S > 0:
        buy.append([i, B_S])
    elif B_S < 0:
        sell.append([i, B_S])
    else:
        hold.append(i)


buy = sorted(buy, key= lambda x:x[1])
buy = buy[::-1]
print("BUY:")
print(buy)

print("------------------------------------------------------------")
sell = sorted(sell, key = lambda x:x[1])
print("SELL:")
print(sell)

print("------------------------------------------------------------")
print("HOLD: ")
print(hold)
