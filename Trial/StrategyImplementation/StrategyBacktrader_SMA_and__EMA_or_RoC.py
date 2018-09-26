from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt


class StrategyBacktrader_SMA_and__EMA_or_RoC(bt.Strategy):
    params = (
        ('sma_timeperiod', 5),
        ('ema_timeperiod', 5),
        ('roc_timeperiod', 5),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.datavol = self.datas[0].volume
        self.datahi = self.datas[0].close
        self.datalo = self.datas[0].close
        self.order = None

        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.sma_timeperiod)
        self.ema = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_timeperiod)
        self.roc = bt.indicators.RateOfChange(self.datas[0], period=self.params.roc_timeperiod)

    def next(self):
        if self.order:
            return

        if not self.position:
            sma_buy = self.dataclose[0] > self.sma[0]
            ema_buy = self.dataclose[0] > self.ema[0]
            roc_buy = self.dataclose[0] > self.roc[0]

            if sma_buy and (ema_buy or roc_buy):
                self.order = self.buy()

        else:
            if self.dataclose[0] < self.sma[0]:
                self.order = self.sell()

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(StrategyBacktrader_SMA_and__EMA_or_RoC)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')
    # datapath = os.path.join(modpath, '../../datas/KMX.csv')

    # Create a Data Feed
    data = bt.feeds.YahooFinanceData(
        dataname="AAPL",
        # Do not pass values before this date
        fromdate=datetime.datetime(2017, 1, 2),
        # Do not pass values before this date
        todate=datetime.datetime(2018, 1, 2),
        # Do not pass values after this date
        reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(50000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # Set the commission
    cerebro.broker.setcommission(commission=0.001)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()
