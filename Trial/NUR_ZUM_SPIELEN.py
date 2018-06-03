# anderer quellen
# import pandas_datareader.data as web
# from datetime import datetime
# start = datetime(2015, 2, 9)
# end = datetime(2017, 5, 24)
# f = web.DataReader('F', 'iex', start, end)

# all symbols
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols

symbols = get_nasdaq_symbols()


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]


B = split_list(symbols.index._data, 30)

stock_list = []
for x in range (0, len(B[0])):
    stock_list.append(str(B[0][x]).replace("$", ""))

# caching
import pandas_datareader.data as web
import datetime
import requests_cache

expire_after = datetime.timedelta(days=3)
session = requests_cache.CachedSession(cache_name='cache', backend='sqlite',
                                       expire_after=expire_after)
start = datetime.datetime(2017, 1, 1)
end = datetime.datetime(2018, 1, 1)
f = web.DataReader(stock_list, 'iex', start, end, session=session)

print(f)
# anderer reader / PARALLEL MEHRER LESEN
# 4.5.2 Fama-French Data (Ken French’s Data Library)
# oder 4.5.11 Quandl
