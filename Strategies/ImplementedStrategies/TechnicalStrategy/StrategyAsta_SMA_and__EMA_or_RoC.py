import traceback

import talib
from Signals.Signals import evaluate_signals
from Utils.CommonUtils import wrapper
from Utils.Logger_Instance import logger
from Signals.Signals import signal_is_volume_high_enough, signal_is_volume_raising, signal_is52_w_high
from Strategies.Abstract_Strategy import Abstract_Strategy


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
