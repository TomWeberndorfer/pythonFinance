# example of optimizing SMA crossover strategy parameters using
# Particle Swarm Optimization in the opptunity python library
# https://github.com/claesenm/optunity

from datetime import datetime
from Utils.GlobalVariables import *
import backtrader as bt
import optunity.metrics

from Backtesting.Backtrader.BacktraderWrapper import BacktraderWrapper
from Backtesting.BacktraderStrategyWrapper import BacktraderStrategyWrapper
from Trial.StrategyImplementation.StrategyBacktrader_SMA_and__EMA_or_RoC import StrategyBacktrader_SMA_and__EMA_or_RoC
from Utils.FileUtils import FileUtils

##################################################
from Utils.CommonUtils import TimeDiffMeasurement

test_filepath = GlobalVariables.get_root_dir() + '\\DataFiles\\TestData\\'
time_measurement = TimeDiffMeasurement()

########################################################################
# source code to evaluate the performance of ASTA-Framework
# with backtrader wrapper to shorten code
# Section 4.3. 	Use Case 2: Kombination und Optimierung einer Strategie
########################################################################
data0 = bt.feeds.YahooFinanceData(dataname='AAPL',
                                  fromdate=datetime(2017, 1, 1),
                                  todate=datetime(2017, 12, 31))


def init_and_run_asta_strategy(sma_timeperiod, ema_timeperiod, roc_timeperiod, stock_data=data0):
    print('sma_timeperiod = %.2f' % sma_timeperiod)
    print('ema_timeperiod = %.2f' % ema_timeperiod)
    print('roc_timeperiod = %.2f' % roc_timeperiod)
    print()

    analysis_parameters = {
        'sma_timeperiod': sma_timeperiod,
        'ema_timeperiod': ema_timeperiod,
        'roc_timeperiod': roc_timeperiod
    }

    backtesting_parameters = {'BacktestingFramework': 'BacktraderWrapper', 'initial_cash': 50000,
                              'trade_commission_percent': 0.001}
    risk_model = {'FixedSizeRiskModel': {'OrderTarget': 'order_target_value', 'TargetValue': 5000}}
    tbt = BacktraderWrapper()

    backtesting_result_instance, res = tbt.run_test([stock_data], "StrategyAsta_SMA_and__EMA_or_RoC",
                                                    backtesting_parameters,
                                                    analysis_parameters,
                                                    risk_model, [])

    return backtesting_result_instance.broker.getvalue()


if __name__ == '__main__':

    for i in range(0, 5):
        time_measurement.restart_time_measurement()
        opt = optunity.maximize(init_and_run_asta_strategy, num_evals=2, sma_timeperiod=[4, 7], ema_timeperiod=[4, 7],
                                roc_timeperiod=[4, 7])

        optimal_pars, details, _ = opt
        print('----------------------')
        print('Optimal Parameters:')
        print('sma_timeperiod = %.2f' % optimal_pars['sma_timeperiod'])
        print('ema_timeperiod = %.2f' % optimal_pars['ema_timeperiod'])
        print('roc_timeperiod = %.2f' % optimal_pars['roc_timeperiod'])

        time_measurement.print_time_diff("Time to get the optimum:")

    time_measurement.print_and_save_mean(test_filepath + "opttest_asta.txt")
