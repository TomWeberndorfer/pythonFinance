# example of optimizing SMA crossover strategy parameters using
# Particle Swarm Optimization in the opptunity python library
# https://github.com/claesenm/optunity

from datetime import datetime

import backtrader as bt
import optunity.metrics

from Backtesting.BacktraderStrategyWrapper import BacktraderStrategyWrapper

data0 = bt.feeds.YahooFinanceData(dataname='AAPL',
                                  fromdate=datetime(2017, 1, 1),
                                  todate=datetime(2017, 12, 31))


def runstrat(sma_timeperiod, ema_timeperiod, roc_timeperiod):
    cerebro = bt.Cerebro()

    print('sma_timeperiod = %.2f' % sma_timeperiod)
    print('ema_timeperiod = %.2f' % ema_timeperiod)
    print('roc_timeperiod = %.2f' % roc_timeperiod)
    print()

    cerebro.addstrategy(BacktraderStrategyWrapper, strategy_to_test="StrategyAsta_SMA_and__EMA_or_RoC",
                        backtesting_parameters={'BacktestingFramework': 'BacktraderWrapper', 'initial_cash': 30000,
                                                'trade_commission_percent': 0.005},
                        analysis_parameters={'sma_timeperiod': sma_timeperiod, 'ema_timeperiod': ema_timeperiod,
                                             'roc_timeperiod': roc_timeperiod},
                        risk_model={'FixedSizeRiskModel': {'OrderTarget': 'order_target_value', 'TargetValue': 2500}},
                        status_update=False)
    cerebro.adddata(data0)
    cerebro.run()
    return cerebro.broker.getvalue()


opt = optunity.maximize(runstrat, num_evals=2, sma_timeperiod=[4, 7], ema_timeperiod=[4, 7], roc_timeperiod=[4, 7])

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
