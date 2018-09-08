import traceback

from Utils.Logger_Instance import logger
from Signals.Signals import signal_is_volume_high_enough, signal_gap_up
from Strategies.Abstract_Strategy import Abstract_Strategy
from Utils.GlobalVariables import *


class GapUpHighVolumeStrategy(Abstract_Strategy):

    def _method_to_execute(self, stock_data_container):
        super()._method_to_execute(stock_data_container)
        self.update_status("GapUpHighVolumeStrategy:")

    @staticmethod
    def get_required_parameters_with_default_parameters():
        data_file_path = GlobalVariables.get_data_files_path()
        strategy_parameter_dict = \
            {'GapUpHighVolumeStrategy': {'min_gap_factor': 1.03}}
        return strategy_parameter_dict

    def add_signals(self, stock_data_container, parameter_dict):
        """
        Abstract_Strategy with gap between last and open and high volume

        :param stock_data_container: stock name
        :param stock_data: stock data
        :param min_gap_factor: minimum gap up factor (ex: 1.03 = 3%)
        :return: stock to buy with as container list
        """
        self.signal_list = [[signal_is_volume_high_enough, stock_data_container.historical_stock_data()],
                            [signal_gap_up, stock_data_container.historical_stock_data(),
                             parameter_dict['min_gap_factor']]
                            ]
