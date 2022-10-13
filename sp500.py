import bs4 as bs 
import requests

class get_SP500():
    response = requests.get("http://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(response.text, 'html.parser')

    symbolslist = soup.select('table')[0].select('tr')[1:]

    symbols = []
    for i, symbol in enumerate(symbolslist):
        tds = symbol.select('td')
        symbols.append(tds[0].select('a')[0].text)
    
    print(*symbols)