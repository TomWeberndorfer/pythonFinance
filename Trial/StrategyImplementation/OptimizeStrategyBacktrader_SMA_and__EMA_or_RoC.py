# example of optimizing SMA crossover strategy parameters using
# Particle Swarm Optimization in the opptunity python library
# https://github.com/claesenm/optunity

from datetime import datetime
from datetime import datetime
import backtrader as bt
import optunity.metrics

from Trial.StrategyImplementation.StrategyBacktrader_SMA_and__EMA_or_RoC import StrategyBacktrader_SMA_and__EMA_or_RoC
##################################################
from Utils.CommonUtils import TimeDiffMeasurement
from Utils.GlobalVariables import *

test_filepath = GlobalVariables.get_root_dir() + '\\DataFiles\\TestData\\'
time_measurement = TimeDiffMeasurement()

########################################################################
# source code to evaluate the performance of ASTA-Framework
# Load 5 Stocks repetitive, 5 times and print the time for each loop
# Section 4.4 Bewertung - Performance
# TODO
########################################################################
from Utils.FileUtils import FileUtils


def init_and_run_backtrader_strategy(sma_timeperiod, ema_timeperiod, roc_timeperiod):
    cerebro = bt.Cerebro()

    print('sma_timeperiod = %.2f' % sma_timeperiod)
    print('ema_timeperiod = %.2f' % ema_timeperiod)
    print('roc_timeperiod = %.2f' % roc_timeperiod)
    print()

    cerebro.addstrategy(StrategyBacktrader_SMA_and__EMA_or_RoC, sma_timeperiod=int(sma_timeperiod),
                        ema_timeperiod=int(ema_timeperiod), roc_timeperiod=int(roc_timeperiod))

    cerebro.adddata(stock_data)
    cerebro.broker.set_cash(50000)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.run()
    return cerebro.broker.getvalue()


if __name__ == '__main__':
    stock_data = bt.feeds.YahooFinanceData(dataname='AAPL',
                                           fromdate=datetime(2017, 1, 1),
                                           todate=datetime(2017, 12, 31))
    for i in range(0, 5):
        time_measurement.restart_time_measurement()

        opt = optunity.maximize(init_and_run_backtrader_strategy, num_evals=2, sma_timeperiod=[4, 7],
                                ema_timeperiod=[4, 7],
                                roc_timeperiod=[4, 7])

        optimal_pars, details, _ = opt
        print('----------------------')
        print('Optimal Parameters:')
        print('sma_timeperiod = %.2f' % optimal_pars['sma_timeperiod'])
        print('ema_timeperiod = %.2f' % optimal_pars['ema_timeperiod'])
        print('roc_timeperiod = %.2f' % optimal_pars['roc_timeperiod'])

        time_measurement.print_time_diff("Time to get the optimum:")

    time_measurement.print_and_save_mean(test_filepath + "opttest_backtrader.txt")

    # cerebro = bt.Cerebro()
    # cerebro.addstrategy(StrategyBacktrader_SMA_and__EMA_or_RoC, sma_timeperiod=optimal_pars['sma_timeperiod'],
    #                     ema_timeperiod=optimal_pars['ema_timeperiod'], roc_timeperiod=optimal_pars['roc_timeperiod'])
    # cerebro.adddata(data0)
    # cerebro.run()
    # cerebro.plot()
