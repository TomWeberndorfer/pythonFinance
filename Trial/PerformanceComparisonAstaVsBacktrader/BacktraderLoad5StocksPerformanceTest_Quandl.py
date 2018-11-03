from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from datetime import datetime
from datetime import timedelta
import backtrader as bt

from Utils.GlobalVariables import GlobalVariables
from Utils.StockDataUtils import convert_backtrader_to_dataframe

########################################################################
# source code to evaluate the performance of Backtrader-Framework
# Load 5 Stocks repetitive, 5 times and print the time for each loop
# Section 4.4 Bewertung - Performance
########################################################################


todate = datetime.now()
fromdate = (todate - timedelta(weeks=52))

symbols = ["AAPL", "FB", "GIS", "GE", "XOM"]

##################################################
from Utils.CommonUtils import TimeDiffMeasurement

test_filepath = GlobalVariables.get_root_dir() + '\\DataFiles\\TestData\\'
time_measurement = TimeDiffMeasurement()
# plot_symbols = []
data_list = []

for i in range(0, 5):
    time_measurement.restart_time_measurement()

    for s in symbols:
        data = bt.feeds.Quandl(dataname=s, fromdate=fromdate, todate=todate)

        # TODO
        if 0:
            df = convert_backtrader_to_dataframe(data)
            data_list.append(data)

    time_measurement.print_time_diff("TimeDiff load 5 stocks backtrader QUANDL:")

time_measurement.print_and_save_mean(test_filepath + "load_5_stocks_test_backtrader_QUANDL.txt")
