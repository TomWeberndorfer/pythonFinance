import datetime as dt
import os
import pickle
import sys
import traceback

import pandas_datareader.data as web
import pandas as pd

from Utils import get_current_function_name, read_and_save_sp500_tickers

filepath = 'C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\'


# read_and_save_sp500_tickers()

#TODO insert into stock screening
def get_data_from_yahoo(tickers_file, stock_dfs_file, reload_sp500=False):
    if reload_sp500:
        read_and_save_sp500_tickers(tickers_file)
    else:
        with open(tickers_file, "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists(stock_dfs_file):
        os.makedirs(stock_dfs_file)

    end = dt.datetime.now()
    start = (end - dt.timedelta(weeks=52))

    for ticker in tickers:

        try:
            # TODO does not reload new data
            if not os.path.exists(stock_dfs_file + '/{}.csv'.format(ticker)):
                df = web.DataReader(ticker, "google", start, end)
                df.to_csv(stock_dfs_file + '/{}.csv'.format(ticker))
                print('Reading {}'.format(ticker))
            else:
                print('Already have {}'.format(ticker))

        except Exception as e:
            sys.stderr.write("EXCEPTION in " + get_current_function_name() + " , " + str(e) + "\n")
            traceback.print_exc()


def get_data_from_google_with_webreader(ticker, stock_dfs_file, reload_sp500=False, reload_stockdata=False):
    # if reload_sp500:
    #     read_and_save_sp500_tickers(tickers_file)
    # else:
    #     with open(tickers_file, "rb") as f:
    #         tickers = pickle.load(f)

    # if not os.path.exists(stock_dfs_file):
    #     os.makedirs(stock_dfs_file)

    df = []

    try:
        # TODO does not reload new data
        if not os.path.exists(stock_dfs_file + '/{}.csv'.format(ticker)) or reload_stockdata:
            end = dt.datetime.now()
            start = (end - dt.timedelta(weeks=52))
            df = web.DataReader(ticker, "google", start, end)
            if len(df) > 0:
                df.to_csv(stock_dfs_file + '/{}.csv'.format(ticker))
                print('FAILED: Reading {}'.format(ticker))
        else:
            #print('Already have {}'.format(ticker))
            df = pd.read_csv(stock_dfs_file + '/{}.csv'.format(ticker))

    except Exception as e:
        sys.stderr.write("EXCEPTION in " + get_current_function_name() + " , " + str(e) + "\n")
        traceback.print_exc()

    return df

#get_data_from_yahoo(filepath + "sp500tickers.pickle", filepath + 'stock_dfs')

#get_data_from_google_with_webreader ("AAPL", filepath + 'stock_dfs')

