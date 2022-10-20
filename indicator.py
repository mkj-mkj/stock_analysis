import numpy
import pandas as pd

def Rate_of_Price_Spread(data): #漲跌幅：((今日收盤價-前日收盤價)/前日收盤價)%
    data['rate_of_price_spread'] = round((((data['Close'] - data['Close'].shift(1)) / data['Close'].shift(1))) * 100, 2)
def MA(data, days): #MA(Moving Average, 移動平均線):n天收盤價的平均值 
    column_name = 'MA_{0}'.format(days)
    data[column_name] = data['Close'].rolling(days).mean()

def EMA(data, days): #EMA(Exponential Moving Average, 指數平滑移動平均線)
                     #今日EMA = 今日收盤價 * α + 昨日EMA * (1-α), α一般取2/(n+1)
    data['EMA'] = data['Close'].ewm(span=days).mean()

def RSI(data, days, adjust=False): #RSI(Related Strength Index, 相對強弱指標):n日漲幅平均值/(n日漲幅平均值+n日跌幅平均值) * 100
                                   #RSI大於50,買方較強；RSO小於50,賣方較強
    delta = data['Close'].diff(1).dropna() 
    price_fall = delta.copy()
    price_raise = delta.copy()

    price_raise[price_raise < 0] = 0 #漲幅
    price_fall[price_fall > 0] = 0  #跌幅

    price_raise_ewm = price_raise.ewm(com=days - 1, adjust=adjust).mean() #漲幅的指數移動平均值
    price_fall_ewm = abs(price_fall.ewm(com=days - 1, adjust=adjust).mean()) #跌幅的指數移動平均值

    data['RSI'] = 100 - 100 / (1 + price_raise_ewm / price_fall_ewm)

def KDJ(data, days): #Stochastic Oscillator(隨機指標), K稱為快速指標, D稱為慢速指標, J為KD值的乖離程度
    #先計算出RSV(Raw Stochastic Value, 未成熟隨機值)
    #RSV = (第n天的收盤價-最近n天內的最低價)/(最近n天內的最高價-最近n天內的最低價) *100
    low_list = data['Close'].rolling(days, min_periods = 1).min() #最低價
    high_list = data['High'].rolling(days, min_periods = 1).max() #最高價

    rsv = ((data['Close'] - low_list) / (high_list - low_list)) * 100

    #K值由RSV的指數移動平均計算得到, 即前一日的K值和當前的RSV值經權重調整後相加得到
    #今天的K值 = 昨天的K值*(2/3) + 今天的RSV值*(1/3)
    #D值由K值的指數移動平均計算得到, 即前一日的D值和當前的K值經權重調整後相加得到
    #今天的D值 = 昨天的D值*(2/3) + 今天的K值*(1/3)
    #J = 3*K - 2*D
    data['K'] = rsv.ewm(com=2, adjust=False).mean()
    data['D'] = data['K'].ewm(com=2, adjust=False).mean()
    data['J'] = data['K'] * 3 - data['D'] * 2

def DIF(data): #DIF為離差值, 利用短期與長期的指數移動平均相減計算出來的
    data['DIF'] = EMA(data, 12) - EMA(data, 26) #一般使用短期為 12 日, 長期為 26 日
                                        
def MACD(data): #計算出DIF後, 再取DIF的移動平均, 就是MACD線
    data['MACD'] = data['DIF'].ewm(span=9).mean() #一般用 DIF 的 9日移動平均

def OBV(data): #OBV(On Balance Volume, 量能潮指標), 依照行情的漲跌來累計市場上美日的成交量值        
    data['Volume_by_Hand'] = data['Volume'] / 1000000 #把單位換成萬手
    data['OBV'] = 0
    for i in range(1, len(data['Close'])): #從第二天開始
        if data['Close'][i] > data['Close'][i-1]: #如果今日收盤大於昨日收盤, 今日OBV=昨日OBV + 今日成交量
            data['OBV'][i] = data['OBV'][i-1] + data['Volume_by_Hand'][i]
        elif data['Close'][i] < data['Close'][i-1]: #如果今日收盤小於昨日收盤, 今日OBV=昨日OBV - 今日成交量
            data['OBV'][i] = data['OBV'][i-1] - data['Volume_by_Hand'][i]
        else: #如果今日收盤等於昨日收盤, 今日OBV=昨日OBV
            data['OBV'][i] = data['OBV'][i-1]

def ATR(data, days): #ATR(Average True Range, 真實波動幅度均值) 首先要計算真實波動幅度, 之後再其結果進行移動平均
                     #波動幅度則是以下面三者中的最大者為準：
                     #1.當天最高點和最低點間的距離
                     #2.前一天收盤價和當天最高價間的距離
                     #3.前一天收盤價和當天最低價間的距離
    for i in range(0, len(data)):
        data.loc[data.index[i], 'TR'] = max((data['High'][i] - data['Low'][i]), (data['Close'].shift(1)[i] - data['High'][i]), (data['Close'].shift(1)[i] - data['Low'][i]))
    
    data['ATR'] = data['TR'].rolling(days).mean()

def Aroon(data, days): #Arron oscillator(阿隆指標), 主要用途是來判斷趨勢的新生, 方向與強度
                       #這個技術指標中包括兩根線：Aroon-up(多方)和Aroon-down(空方)
                       #Aroon-up= ((n-n天內最高價發生日到今天的天數)/n) *100
                       #Aroon-down= ((n-n天內最低價發生日到今天的天數)/n) *100
    data['Aroon_up'] = 100 * data['High'].rolling(days).apply(lambda x: x.argmax()) / days
    data['Aroon_down'] = 100 * data['Low'].rolling(days).apply(lambda x: x.argmin()) / days

def CCI(data, days): #CCI(Channel Commodity Index, 順勢指標), CCI假設價格是有一定的週期性, 把價格與股價平均區間的偏離程度以正負值在圖表上展示
                     #CCI=(TP-MA)/0.015 *MD
                     #TP=(最高價+最低價+收盤價)/3
                     #SMA=n日間的TP移動平均
                     #MD=TP-MA的平均偏差
    data['TP'] = (data['High'] + data['Low'] + data['Close']) / 3
    data['TP_SMA'] = data['TP'].rolling(days).mean()
    data['MAD'] = data['TP'].rolling(days).apply(lambda x: pd.Series(x).mad())
    data['CCI'] = (data['TP'] - data['TP_SMA']) / (0.015 * data['MAD']) 

def Bollinger(data, days): #B-Band(Bollinger Bands, 布林通道), 以中央的移動平均線加減兩個標準差（σ）所算出
                           #布林通道"收窄"和"擴大"被當作是支撐位和阻力位的指標
    MA(data, days) #先取平均移動線
    column_name = 'MA_{0}'.format(days)
    data['std'] = data['Close'].rolling(days).std() #取週期內收盤價的標準差
    data['Upper_Bollinger'] = data[column_name] + data['std'] * 2
    data['Lower_Bollinger'] = data[column_name] -   data['std'] * 2

def Williams(data, days): #Williams%R(威廉指標), 利用當日收盤價判斷多空去向
                          #Williams小於50時, 多方較強; Williams大於50時, 空方較強
                          #Williams = (最近n天內的最高價-第n天的收盤價)/(最近n天內的最高價-最近n天內的最低價) *100
    data['low_list'] = data['Close'].rolling(days, min_periods = 1).min() #最低價
    data['high_list'] = data['High'].rolling(days, min_periods = 1).max() #最高價
    data['Williams'] = ((data['high_list'] - data['Close']) / (data['high_list'] - data['low_list'])) * 100