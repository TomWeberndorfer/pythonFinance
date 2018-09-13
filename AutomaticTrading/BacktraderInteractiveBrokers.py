from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
from Utils.GlobalVariables import GlobalVariables


# TODO: see:
# https://medium.com/@danjrod/interactive-brokers-in-python-with-backtrader-23dea376b2fc
class St(bt.Strategy):
    def logdata(self):
        txt = []
        txt.append('{}'.format(len(self)))

        txt.append('{}'.format(
            self.data.datetime.datetime(0).isoformat())
        )
        txt.append('{:.2f}'.format(self.data.open[0]))
        txt.append('{:.2f}'.format(self.data.high[0]))
        txt.append('{:.2f}'.format(self.data.low[0]))
        txt.append('{:.2f}'.format(self.data.close[0]))
        txt.append('{:.2f}'.format(self.data.volume[0]))
        print(','.join(txt))

    def next(self):
        self.logdata()


def run(args=None):
    cerebro = bt.Cerebro(stdstats=False)
    store = bt.stores.IBStore(port=GlobalVariables.get_broker_demo_port())
    data = store.getdata(dataname='TWTR',
                         timeframe=bt.TimeFrame.Ticks)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds,
                         compression=10)
    cerebro.addstrategy(St)
    cerebro.run()


if __name__ == '__main__':
    run()
