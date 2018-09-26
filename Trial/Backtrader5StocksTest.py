from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from datetime import timedelta
import argparse
import datetime
import random

import backtrader as bt
from datetime import datetime
from pandas import DataFrame

from Utils.GlobalVariables import *
from plotly import graph_objs as go, plotly as py

from Utils.StockDataUtils import convert_backtrader_to_dataframe

todate = datetime.now()
fromdate = (todate - timedelta(weeks=5))

symbols = ["AAPL"]  # ,"FB","GIS","GE", "XOM"]
start_time = datetime.now()

# plot_symbols = []
data_list = []
for s in symbols:
    data = bt.feeds.Quandl(dataname=s, fromdate=fromdate, todate='2018-09-21')
    # df = convert_backtrader_to_dataframe(data)
    # data_list.append(data)

end_time = datetime.now()
time_diff = end_time - start_time

print("Time to get the stocks:" + (str(time_diff)))

print()
