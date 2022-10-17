import bs4 as bs 
import requests

def get_SP500():
    response = requests.get("http://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(response.text, 'html.parser')

    symbolslist = soup.select('table')[0].select('tr')[1:]

    symbols = []
    for i, symbol in enumerate(symbolslist):
        tds = symbol.select('td')
        symbols.append(tds[0].select('a')[0].text)
    
    sp_file = open('sp500.txt', 'w')
    for i in range(0, len(symbols)):
        if (i + 1) % 10 == 0:
            sp_file.write("{}\n".format(symbols[i]))
        else:
            sp_file.write("{} ".format(symbols[i]))
    print(*symbols)

get_SP500()