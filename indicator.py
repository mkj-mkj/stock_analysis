def Rate_of_Price_Spread(data): #漲跌幅：((今日收盤價-前日收盤價)/前日收盤價)%
    rate_of_price_spread = round((((data['Close'] - data['Close'].shift(1)) / data['Close'].shift(1))) * 100, 2)
    return rate_of_price_spread

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

    RSI = 100 - 100 / (1 + price_raise_ewm / price_fall_ewm)
    return RSI

def KDJ(data, days): #隨機指標, K稱為快速指標, D稱為慢速指標
    #先計算出RSV(Raw Stochastic Value, 未成熟隨機值)
    #RSV = (第n天的收盤價-最近n天內的最低價)/(最近n天內的最高價-最近n天內的最低價) *100
    low_list = data['Close'].rolling(days, min_periods = 1).min() #最低價
    high_list = data['High'].rolling(days, min_periods = 1).max() #最高價

    rsv = ((data['Close'] - low_list) / (high_list - low_list)) * 100

    #K值由RSV的指數移動平均計算得到, 即前一日的K值和當前的RSV值經權重調整後相加得到
    #今天的K值 = 昨天的K值*(2/3) + 今天的RSV值*(1/3)
    #D值由K值的指數移動平均計算得到, 即前一日的D值和當前的K值經權重調整後相加得到
    #今天的D值 = 昨天的D值*(2/3) + 今天的K值*(1/3)
    #J值標示了KD值的乖離程度
    #J = 3*K - 2*D
    data['K'] = rsv.ewm(com=2, adjust=False).mean()
    data['D'] = data['K'].ewm(com=2, adjust=False).mean()
    data['J'] = data['K'] * 3 - data['D'] * 2
    return data['K'], data['D'], data['J']

def DIF(data): #DIF為離差值, 利用短期與長期的指數移動平均相減計算出來的
    data['DIF'] = EMA(data, 12) - EMA(data, 26) #一般使用短期為 12 日, 長期為 26 日
                                        
def MACD(data): #計算出DIF後, 再取DIF的移動平均, 就是MACD線
    data['MACD'] = data['DIF'].ewm(span=9).mean() #一般用 DIF 的 9日移動平均