from datetime import datetime
import backtrader as bt

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

################################
# https://ntguardian.wordpress.com/2017/06/12/getting-started-with-backtrader/
################################

class SmaCross(bt.SignalStrategy):
    params = (('pfast', 10), ('pslow', 30),)

    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=self.p.pfast), bt.ind.SMA(period=self.p.pslow)
        self.signal_add(bt.SIGNAL_LONG, bt.ind.CrossOver(sma1, sma2))


modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
datapath = os.path.join(modpath, '../../datas/KMX.csv')

data = bt.feeds.YahooFinanceData(
    dataname=datapath,
    # Do not pass values before this date
    fromdate=datetime.datetime(2017, 1, 2),
    # Do not pass values before this date
    todate=datetime.datetime(2018, 1, 2),
    # Do not pass values after this date
    reverse=False)

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2016, 10, 31)
#symbols = ["AAPL", "GOOG", "MSFT", "AMZN", "YHOO", "SNY", "NTDOY", "IBM", "HPQ", "QCOM", "NVDA"]
symbols = ["AAPL", "GOOG"]
#plot_symbols = ["AAPL", "GOOG", "NVDA"]
#plot_symbols = []
cerebro = bt.Cerebro()

for s in symbols:
    data = bt.feeds.YahooFinanceData(dataname=s, fromdate=start, todate=end)
    cerebro.adddata(data)




cerebro.addstrategy(SmaCross)
cerebro.run()
cerebro.plot()