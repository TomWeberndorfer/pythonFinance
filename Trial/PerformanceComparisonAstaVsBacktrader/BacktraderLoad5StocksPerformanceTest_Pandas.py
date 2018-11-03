import datetime as dt
import traceback
from datetime import datetime
from pandas_datareader import data

from DataReading.Abstract_StockDataReader import Abstract_StockDataReader
from Utils.Logger_Instance import logger
from Utils.GlobalVariables import *

end = dt.datetime.now()
start = (end - dt.timedelta(weeks=52))

##################################################
from Utils.CommonUtils import TimeDiffMeasurement

test_filepath = GlobalVariables.get_root_dir() + '\\DataFiles\\TestData\\'
time_measurement = TimeDiffMeasurement()

for i in range(0, 5):
    time_measurement.restart_time_measurement()

    symbols = ["AAPL", "FB", "GIS", "GE", "XOM"]

    for s in symbols:
        df = data.DataReader(s, 'iex', start, end, 3, 0.05)

    time_measurement.print_time_diff("TimeDiff load 5 stocks backtrader PANDAS:")

time_measurement.print_and_save_mean(test_filepath + "load_5_stocks_test_backtrader_PANDAS.txt")
