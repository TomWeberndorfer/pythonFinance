import datetime as dt
import quandl
from datetime import datetime
from datetime import timedelta

from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from DataReading.HistoricalDataReaders.HistoricalDataReaderQuandl import HistoricalDataReaderQuandl
from Utils.CommonUtils import CommonUtils

end = dt.datetime.now()
start = (end - dt.timedelta(weeks=52))

# df = data.DataReader(ticker_exchange, data_source, start, end, 3, 0.05)

import quandl

quandl.ApiConfig.api_key = 'Gq6_HqRdHa8KWKV4r7-F'

symbols = ["AAPL", "FB", "GIS", "GE", "XOM"]
# symbols = CommonUtils.read_table_columns_from_webpage_as_list("http://en.wikipedia.org/wiki/List_of_S%26P_500_companies", "table", "class", "wikitable sortable", 0, 1, "en")

stock_data_container_list = []
apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
fb_cont = StockDataContainer("Facebook, Inc.", "FB", "")
gis_cont = StockDataContainer("General Mills, Inc.", "GIS", "")
ge_cont = StockDataContainer("General Electric Company.", "GE", "")
xom_cont = StockDataContainer("Exxon Mobile Corporation", "XOM", "")

stock_data_container_list.append(apple_stock_data_container)

if 1:
    stock_data_container_list.append(fb_cont)
    stock_data_container_list.append(gis_cont)
    stock_data_container_list.append(ge_cont)
    stock_data_container_list.append(xom_cont)

start_time = datetime.now()
hdr = HistoricalDataReaderQuandl(stock_data_container_list, True, {})
sdcl = hdr.read_data()

end_time = datetime.now()
time_diff = end_time - start_time
print("Time to get the stocks:" + (str(time_diff)))
