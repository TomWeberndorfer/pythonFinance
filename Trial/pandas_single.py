import datetime as dt
import traceback
from datetime import datetime
from pandas_datareader import data

from DataReading.Abstract_StockDataReader import Abstract_StockDataReader
from Utils.Logger_Instance import logger
from Utils.GlobalVariables import *

end = dt.datetime.now()
start = (end - dt.timedelta(weeks=52))

start_time = datetime.now()

symbols = ["AAPL", "FB", "GIS", "GE", "XOM"]

# plot_symbols = []
data_list = []
for s in symbols:
    df = data.DataReader(s, 'iex', start, end, 3, 0.05)

end_time = datetime.now()
time_diff = end_time - start_time
print("Time to get the stocks:" + (str(time_diff)))
