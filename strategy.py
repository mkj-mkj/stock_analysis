from indicator import * 
import numpy as np
import pandas as pd

def strategy_beta(data):
    RSI(data, 14)
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

def strategy_advanced(data):
    RSI(data, 14)
    Bollinger(data, 14)
    Williams(data, 14)
    Aroon(data, 14)
    data['Buy&Sell'] = ""
    B_S = 0
    
    if(data['Williams'] > 50):
        B_S += 1
    elif(data['Williams'] < 50):
        B_S -= 1

    if(data['Aroon_up'] > data['Aroon_down']):
        B_S += 1
    elif(data['Aroon_up'] < data['Aroon_down']):
        B_S -= 1

    for i in range(3, len(data)):
        #RSI連續3天小於50且連續上升3天, 則買入
        if (((data['RSI'])[i] < 50) and (data['RSI'])[i-1] < 50) and ((data['RSI'])[i-2] < 50) and (((data['RSI'])[i] > (data['RSI'])[i-1]) and (((data['RSI'])[i] > (data['RSI'])[i-1]))):
            if(data['Close'] <= data['Upper Bollinger']):
                B_S += 1
            #RSI連續3天大於50且連續下降3天, 則賣出
        elif (((data['RSI'])[i] > 50) and (data['RSI'])[i-1] > 50) and ((data['RSI'])[i-2] > 50) and (((data['RSI'])[i] < (data['RSI'])[i-1]) and (((data['RSI'])[i] < (data['RSI'])[i-1]))):
            if(data['Close'] >= data['Lower Bollinger']):
                B_S -= 1
    
    for i in range(len(data)):
        if(data['B_S'][i] >= 1):
            data['Buy&Sell'][i] = "Buy"
        elif(data['B_S'][i] <= -1):
            data['Buy&Sell'][i] = "Sell"

    return 0                                                                                            