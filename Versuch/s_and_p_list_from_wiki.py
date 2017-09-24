import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests

filepath = 'C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\'

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    return tickers


# save_sp500_tickers()

#TODO insert into stock screening
def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists(filepath + 'stock_dfs'):
        os.makedirs(filepath + 'stock_dfs')

    end = dt.datetime.now()
    start = (end - dt.timedelta(weeks=52))


    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists(filepath + 'stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, "google", start, end)
            df.to_csv(filepath + 'stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))




get_data_from_yahoo(True)
