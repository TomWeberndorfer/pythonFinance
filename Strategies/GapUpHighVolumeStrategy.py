import sys

from Signals.Signals import signal_is_volume_high_enough, signal_gap_up
from Strategies.Abstract_Strategy import Abstract_Strategy
from Utils.common_utils import CommonUtils, get_current_function_name


class GapUpHighVolumeStrategy(Abstract_Strategy):

    def _method_to_execute(self, stock_data_container):
        try:
            if len(stock_data_container.historical_stock_data) > 0:
                result = self.strat_gap_up__hi_volume(stock_data_container, self.parameter_dict)

                if result is not None:
                    self.result_list.append(result)
        except Exception as e:
            sys.stderr.write("Exception:  " + str(e) + "\n")

    def strat_gap_up__hi_volume(self, stock_data_container, parameter_dict):
        """
        Abstract_Strategy with gap between last and open and high volume

        :param stock_data_container: stock name
        :param stock_data: stock data
        :param min_gap_factor: minimum gap up factor (ex: 1.03 = 3%)
        :return: stock to buy with {'buy', 'stock_name', 'sb', 'sl'}
        """

        if stock_data_container is None or parameter_dict['min_gap_factor'] is None:
            raise NotImplementedError

        if not signal_is_volume_high_enough(stock_data_container.historical_stock_data):
            return None

        if not signal_gap_up(stock_data_container.historical_stock_data, parameter_dict['min_gap_factor']):
            return None

        return stock_data_container