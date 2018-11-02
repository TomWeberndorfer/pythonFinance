# example of optimizing SMA crossover strategy parameters using
# Particle Swarm Optimization in the opptunity python library
# https://github.com/claesenm/optunity

from datetime import datetime
from datetime import datetime
import backtrader as bt
import optunity.metrics

from Trial.StrategyImplementation.StrategyBacktrader_SMA_and__EMA_or_RoC import StrategyBacktrader_SMA_and__EMA_or_RoC

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

    cerebro.adddata(apple_data)
    # TODO set cash
    # todo  add analyzers
    cerebro.run()
    return cerebro.broker.getvalue()


if __name__ == '__main__':
    apple_data = bt.feeds.YahooFinanceData(dataname='AAPL',
                                           fromdate=datetime(2017, 1, 1),
                                           todate=datetime(2017, 12, 31))
    for i in range(0, 5):
        start_time = datetime.now()

        opt = optunity.maximize(init_and_run_backtrader_strategy, num_evals=2, sma_timeperiod=[4, 7],
                                ema_timeperiod=[4, 7],
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

        FileUtils.append_text_list_to_file(text_list, "C:\\temp\\opttest_backtrader.txt", False)

    # cerebro = bt.Cerebro()
    # cerebro.addstrategy(StrategyBacktrader_SMA_and__EMA_or_RoC, sma_timeperiod=optimal_pars['sma_timeperiod'],
    #                     ema_timeperiod=optimal_pars['ema_timeperiod'], roc_timeperiod=optimal_pars['roc_timeperiod'])
    # cerebro.adddata(data0)
    # cerebro.run()
    # cerebro.plot()
