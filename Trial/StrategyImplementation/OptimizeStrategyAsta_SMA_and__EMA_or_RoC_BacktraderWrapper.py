# example of optimizing SMA crossover strategy parameters using
# Particle Swarm Optimization in the opptunity python library
# https://github.com/claesenm/optunity

from datetime import datetime

import backtrader as bt
import optunity.metrics

from Backtesting.Backtrader.BacktraderWrapper import BacktraderWrapper
from Backtesting.BacktraderStrategyWrapper import BacktraderStrategyWrapper
from Trial.StrategyImplementation.StrategyBacktrader_SMA_and__EMA_or_RoC import StrategyBacktrader_SMA_and__EMA_or_RoC
from Utils.FileUtils import FileUtils

data0 = bt.feeds.YahooFinanceData(dataname='AAPL',
                                  fromdate=datetime(2017, 1, 1),
                                  todate=datetime(2017, 12, 31))


########################################################################
# source code to evaluate the performance of ASTA-Framework
# with backtrader wrapper to shorten code
# Section 4.3. 	Use Case 2: Kombination und Optimierung einer Strategie
########################################################################

def runstrat(sma_timeperiod, ema_timeperiod, roc_timeperiod):
    print('sma_timeperiod = %.2f' % sma_timeperiod)
    print('ema_timeperiod = %.2f' % ema_timeperiod)
    print('roc_timeperiod = %.2f' % roc_timeperiod)
    print()

    analysis_parameters = {
        'sma_timeperiod': sma_timeperiod,
        'ema_timeperiod': ema_timeperiod,
        'roc_timeperiod': roc_timeperiod
    }

    backtesting_parameters = {'BacktestingFramework': 'BacktraderWrapper', 'initial_cash': 30000,
                              'trade_commission_percent': 0.005}

    risk_model = {'FixedSizeRiskModel': {'OrderTarget': 'order_target_value', 'TargetValue': 2500}}

    tbt = BacktraderWrapper()

    backtesting_result_instance, res = tbt.run_test([data0], "StrategyAsta_SMA_and__EMA_or_RoC", backtesting_parameters,
                                                    analysis_parameters,
                                                    risk_model, [])

    return backtesting_result_instance.broker.getvalue()


if __name__ == '__main__':
    for i in range(0, 5):
        start_time = datetime.now()
        opt = optunity.maximize(runstrat, num_evals=2, sma_timeperiod=[4, 7], ema_timeperiod=[4, 7],
                                roc_timeperiod=[4, 7])

        optimal_pars, details, _ = opt
        end_time = datetime.now()
        time_diff = end_time - start_time
        print('----------------------')
        print("Time to get the optimum:" + (str(time_diff)))
        print('Optimal Parameters:')
        print('sma_timeperiod = %.2f' % optimal_pars['sma_timeperiod'])
        print('ema_timeperiod = %.2f' % optimal_pars['ema_timeperiod'])
        print('roc_timeperiod = %.2f' % optimal_pars['roc_timeperiod'])

        text_list = [str(time_diff), str(optimal_pars['sma_timeperiod']), str(optimal_pars['ema_timeperiod']),
                     str(optimal_pars['roc_timeperiod']), "\n"]

        FileUtils.append_text_list_to_file(text_list, "C:\\temp\\opttest_asta.txt", False)

    # cerebro = bt.Cerebro()
    # cerebro.addstrategy(StrategyBacktrader_SMA_and__EMA_or_RoC, sma_timeperiod=optimal_pars['sma_timeperiod'],
    #                     ema_timeperiod=optimal_pars['ema_timeperiod'], roc_timeperiod=optimal_pars['roc_timeperiod'])
    # cerebro.adddata(data0)
    # cerebro.run()
    # cerebro.plot()
