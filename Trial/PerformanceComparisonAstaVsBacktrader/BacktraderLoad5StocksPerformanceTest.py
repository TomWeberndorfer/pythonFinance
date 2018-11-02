from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from datetime import datetime
from datetime import timedelta
import backtrader as bt
from Utils.StockDataUtils import convert_backtrader_to_dataframe

########################################################################
# source code to evaluate the performance of Backtrader-Framework
# Load 5 Stocks repetitive, 5 times and print the time for each loop
# Section 4.4 Bewertung - Performance
########################################################################


todate = datetime.now()
fromdate = (todate - timedelta(weeks=52))

symbols = ["AAPL", "FB", "GIS", "GE", "XOM"]

for i in range(0, 5):
    start_time = datetime.now()

    # plot_symbols = []
    data_list = []
    for s in symbols:
        data = bt.feeds.Quandl(dataname=s, fromdate=fromdate, todate=todate)

        if 0:
            df = convert_backtrader_to_dataframe(data)

        data_list.append(data)

    print('----------------------')
    print("Time diff:" + (str(datetime.now() - start_time)))
    print('----------------------')

print()
