from datetime import datetime

import talib
from Utils.GlobalVariables import *

from Strategies.Abstract_Strategy import Abstract_Strategy
from Trial.StrategyImplementation.OptimizeStrategyAsta_SMA_and__EMA_or_RoC_BacktraderWrapper import init_and_run_asta_strategy


class StrategyAsta_SMA_and__EMA_or_RoC(Abstract_Strategy):

    @staticmethod
    def get_required_parameters_with_default_parameters():
        return {
            'StrategyAsta_SMA_and__EMA_or_RoC': {
                'sma_timeperiod': 5,
                'ema_timeperiod': 5,
                'roc_timeperiod': 5}
        }

    def _method_to_execute(self, stock_data_container):
        data_close = stock_data_container.historical_stock_data().close
        sma_result = talib.SMA(data_close, self.analysis_parameters['sma_timeperiod'])
        ema_result = talib.EMA(data_close, self.analysis_parameters['ema_timeperiod'])
        roc_result = talib.ROC(data_close, self.analysis_parameters['roc_timeperiod'])
        latest_data_close = data_close.iloc[-1]

        sma_buy = latest_data_close > sma_result.iloc[-1]
        ema_buy = latest_data_close > ema_result.iloc[-1]
        roc_buy = latest_data_close > roc_result.iloc[-1]

        if sma_buy and (ema_buy or roc_buy):
            stock_data_container.update_used_strategy_and_recommendation(self.__class__.__name__, "BUY")
            self.result_list.append(stock_data_container)


if __name__ == '__main__':

    test_filepath = GlobalVariables.get_root_dir() + '\\DataFiles\\TestData\\'

    # Create a Data Feed
    import backtrader as bt

    data0 = bt.feeds.YahooFinanceData(dataname='AAPL',
                                      fromdate=datetime(2017, 1, 1),
                                      todate=datetime(2017, 12, 31))
    ##################################################
    from Utils.CommonUtils import TimeDiffMeasurement

    time_measurement = TimeDiffMeasurement()
    for i in range(0, 5):
        time_measurement.restart_time_measurement()

        portfolio_value = init_and_run_asta_strategy(5, 5, 5, data0)
        print('Final Portfolio Value: %.2f' % portfolio_value)
        time_measurement.print_time_diff("TimeDiff ASTA backtesting:")

    time_measurement.print_and_save_mean(test_filepath + "strat_test_asta.txt")
