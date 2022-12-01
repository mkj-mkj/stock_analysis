from indicator import * 
import numpy as np
import pandas as pd

def strategy_beta(data, period):
    RSI(data, period)
    data['Buy&Sell'] = ""
    B_S = 0
    for i in range(3, len(data)):
        #RSI連續3天小於50且連續上升3天, 則買入
        if (((data['RSI'])[i] < 50) and (data['RSI'])[i-1] < 50) and ((data['RSI'])[i-2] < 50) and (((data['RSI'])[i] > (data['RSI'])[i-1]) and (((data['RSI'])[i] > (data['RSI'])[i-1]))):
            (data['Buy&Sell'])[i] = 'Buy'
            B_S += 1
            #RSI連續3天大於50且連續下降3天, 則賣出
        elif (((data['RSI'])[i] > 50) and (data['RSI'])[i-1] > 50) and ((data['RSI'])[i-2] > 50) and (((data['RSI'])[i] < (data['RSI'])[i-1]) and (((data['RSI'])[i] < (data['RSI'])[i-1]))):
            (data['Buy&Sell'])[i] = 'Sell'
            B_S -= 1
    return B_S