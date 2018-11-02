# example of optimizing SMA crossover strategy parameters using
# Particle Swarm Optimization in the opptunity python library
# https://github.com/claesenm/optunity

from datetime import datetime
import backtrader as bt

import optunity
import optunity.metrics


class SmaCross(bt.SignalStrategy):
    params = (
        ('sma1', 10),
        ('sma2', 30),
    )

    def __init__(self):
        SMA1 = bt.ind.SMA(period=int(self.params.sma1))
        SMA2 = bt.ind.SMA(period=int(self.params.sma2))
        crossover = bt.ind.CrossOver(SMA1, SMA2)
        self.signal_add(bt.SIGNAL_LONG, crossover)


data0 = bt.feeds.YahooFinanceData(dataname='AAPL',
                                  fromdate=datetime(2011, 1, 1),
                                  todate=datetime(2011, 12, 31))


def runstrat(sma1, sma2):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross, sma1=sma1, sma2=sma2)
    print('Evaluate sma1:' + str(sma1) + ', sma2:' + str(sma2))

    cerebro.adddata(data0)
    cerebro.run()
    return cerebro.broker.getvalue()


opt = optunity.maximize(runstrat, num_evals=5, sma1=[2, 55], sma2=[2, 55])

optimal_pars, details, _ = opt
print('----------------------')
print('Optimal Parameters:')
print('sma1 = %.2f' % optimal_pars['sma1'])
print('sma2 = %.2f' % optimal_pars['sma2'])

cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross, sma1=optimal_pars['sma1'], sma2=optimal_pars['sma2'])
cerebro.adddata(data0)
cerebro.run()
cerebro.plot()
