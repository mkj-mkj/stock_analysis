def read_sp500():
    file = open('sp500.txt', 'r')
    symbols_list = []
    symbols = file.readline()
    for i in symbols.split():
        symbols_list.append(i)

    while(symbols):
        symbols = file.readline()
        for i in symbols.split():
            symbols_list.append(i)

    return symbols_list