'''
Author: www.backtest-rookies.com

MIT License

Copyright (c) 2017 backtest-rookies.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import backtrader as bt
from datetime import datetime
from datetime import timedelta

from Utils.CommonUtils import CommonUtils
from Utils.StockDataUtils import convert_backtrader_to_dataframe


class firstStrategy(bt.Strategy):

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=21)

    def next(self):
        for i, hist_data in enumerate(self.datas):
            stock_data_container_list = []
            date_time = self.datetime.date()
            stock_name = hist_data._name

            df1 = convert_backtrader_to_dataframe(hist_data)
            print()
        pass


# Variable for our starting cash
startcash = 10000

# Create an instance of cerebro
cerebro = bt.Cerebro()

# Add our strategy
cerebro.addstrategy(firstStrategy)

symbols = CommonUtils.read_table_columns_from_webpage_as_list(
    "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies", "table", "class", "wikitable sortable", 0, 1, "en")

# symbols = ["AAPL" ,"FB","GIS","GE", "XOM"]
start_time = datetime.now()

end = datetime.now()
start = (end - timedelta(weeks=52))

start_time = datetime.now()
# plot_symbols = []
data_list = []
for s in symbols:
    data = bt.feeds.Quandl(dataname=s, fromdate=start, todate=end)
    cerebro.adddata(data)

end_time = datetime.now()
time_diff = end_time - start_time
print("Time to get the stocks:" + (str(time_diff)))

# cerebro.broker.setcash(startcash)
# cerebro.run()
# cerebro.plot(style='candlestick')
