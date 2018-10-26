import traceback

from Utils.CommonUtils import wrapper
from Utils.Logger_Instance import logger
from Signals.Signals import signal_is_volume_high_enough, signal_is_volume_raising, signal_is52_w_high
from Strategies.Abstract_Strategy import Abstract_Strategy


class W52HighTechnicalStrategy(Abstract_Strategy):

    def _method_to_execute(self, stock_data_container):
        super()._method_to_execute(stock_data_container)
        self.update_status("W52HighTechnicalStrategy:")

    def add_signals(self, stock_data_container, parameter_dict):
        """
        Check 52 week High, raising volume, and high enough volume

        :param  get_stock_name: name of the stock
        :param  stock52_w_data: stock data
        :param  check_days: number of days to check
        :param  min_cnt: min higher days within check days
        :param min_vol_dev_fact:
        :param within52w_high_fact:: factor current data within 52 w high (ex: currVal > (Max * 0.98))

        :return: stock to buy with {'buy', 'get_stock_name', 'sb', 'sl'}
        """
        self.signal_list = [[signal_is_volume_high_enough, stock_data_container.historical_stock_data()],
                            [signal_is_volume_raising, stock_data_container.historical_stock_data(),
                             parameter_dict['check_days'],
                             parameter_dict['min_cnt'], parameter_dict['min_vol_dev_fact']],
                            [signal_is52_w_high, stock_data_container.historical_stock_data(),
                             parameter_dict['within52w_high_fact']]]

    @staticmethod
    def get_required_parameters_with_default_parameters():
        strategy_parameter_dict = \
            {'W52HighTechnicalStrategy':
                 {'check_days': 7,
                  'min_cnt': 3,
                  'min_vol_dev_fact': 1.2,
                  'within52w_high_fact': 0.98,
                  'data_readers': {'HistoricalDataReader': {
                      'weeks_delta': 52,
                      'data_source': 'iex',
                      'reload_data': True,
                      'ticker_needed': True}}}

             }
        return strategy_parameter_dict
