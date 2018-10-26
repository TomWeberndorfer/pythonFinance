# example of optimizing SMA crossover strategy parameters using
# Particle Swarm Optimization in the opptunity python library
# https://github.com/claesenm/optunity

from datetime import datetime

import backtrader as bt
import optunity.metrics

from Trial.StrategyImplementation.StrategyBacktrader_SMA_and__EMA_or_RoC import StrategyBacktrader_SMA_and__EMA_or_RoC


def init_and_run_backtrader_strategy(sma_timeperiod, ema_timeperiod, roc_timeperiod):
    cerebro = bt.Cerebro()

    print('sma_timeperiod = %.2f' % sma_timeperiod)
    print('ema_timeperiod = %.2f' % ema_timeperiod)
    print('roc_timeperiod = %.2f' % roc_timeperiod)
    print()

    cerebro.addstrategy(StrategyBacktrader_SMA_and__EMA_or_RoC, sma_timeperiod=int(sma_timeperiod),
                        ema_timeperiod=int(ema_timeperiod), roc_timeperiod=int(roc_timeperiod))

    cerebro.adddata(apple_data)
    cerebro.run()
    return cerebro.broker.getvalue()


apple_data = bt.feeds.YahooFinanceData(dataname='AAPL',
                                       fromdate=datetime(2017, 1, 1),
                                       todate=datetime(2017, 12, 31))

opt = optunity.maximize(init_and_run_backtrader_strategy, num_evals=2, sma_timeperiod=[4, 7],
                        ema_timeperiod=[4, 7],
                        roc_timeperiod=[4, 7])

optimal_pars, details, _ = opt
print('Optimal Parameters:')
print('sma_timeperiod = %.2f' % optimal_pars['sma_timeperiod'])
print('ema_timeperiod = %.2f' % optimal_pars['ema_timeperiod'])
print('roc_timeperiod = %.2f' % optimal_pars['roc_timeperiod'])

# cerebro = bt.Cerebro()
# cerebro.addstrategy(StrategyBacktrader_SMA_and__EMA_or_RoC, sma_timeperiod=optimal_pars['sma_timeperiod'],
#                     ema_timeperiod=optimal_pars['ema_timeperiod'], roc_timeperiod=optimal_pars['roc_timeperiod'])
# cerebro.adddata(data0)
# cerebro.run()
# cerebro.plot()