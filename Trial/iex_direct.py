from iexfinance import get_historical_data
from datetime import datetime

symbols = ["AAPL", "FB", "GIS", "GE", "XOM"]
start_time = datetime.now()

start = datetime(2017, 2, 9)
end = datetime(2017, 5, 24)

start_time = datetime.now()
# plot_symbols = []
data_list = []
for s in symbols:
    # data = bt.feeds.Quandl(dataname=s, fromdate=start, todate=end)
    df = get_historical_data(s, start=start, end=end, output_format='pandas')

print("Time to get the stocks:" + (str(datetime.now() - start_time)))
