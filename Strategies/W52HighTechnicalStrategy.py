import inspect
import os
import sys
import threading
import traceback
from datetime import datetime, timedelta

from Signals.Signals import signal_is_volume_high_enough, signal_is_volume_raising, signal_is52_w_high
from Strategies.Strategy import Strategy
from Utils.common_utils import split_list, print_stocks_to_buy, calculate_stopbuy_and_stoploss, \
    get_current_function_name, CommonUtils
# from Utils.file_utils import read_tickers_from_file, append_to_file
from Utils.file_utils import FileUtils

# TODO parameter aus self statt da oben --> parameter_dict.news_threshold
# news_threshold = 0.5
##########################

# from directory UnitTests to --> root folder with: ..\\..\\
# TODO übergeben
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class W52HighTechnicalStrategy(Strategy):

    def _method_to_execute(self, stock_data_container):
        try:
            if len(stock_data_container.historical_stock_data) > 0:
                result = self._strat_52_w_hi_hi_volume(stock_data_container, self.parameter_dict)

                if result is not None:
                    self.result_list.append(result)
        except Exception as e:
            sys.stderr.write("Exception:  " + str(e) + "\n")

        self.update_status("W52HighTechnicalStrategy:")

    def _strat_52_w_hi_hi_volume(self, stock_data_container, parameter_dict):
        """
        Check 52 week High, raising volume, and high enough volume

        :param  stock_name: name of the stock
        :param  stock52_w_data: stock data
        :param  check_days: number of days to check
        :param  min_cnt: min higher days within check days
        :param min_vol_dev_fact:
        :param within52w_high_fact:: factor current data within 52 w high (ex: currVal > (Max * 0.98))

        :return: stock to buy with {'buy', 'stock_name', 'sb', 'sl'}
        """
        if stock_data_container.stock_name is None \
                or stock_data_container.historical_stock_data is None \
                or parameter_dict['check_days'] is None \
                or parameter_dict['min_cnt'] is None \
                or parameter_dict['min_vol_dev_fact'] is None \
                or parameter_dict['within52w_high_fact'] is None:
            raise NotImplementedError

        if parameter_dict['min_vol_dev_fact'] < 1:
            raise AttributeError("parameter min_vol_dev_fact must be higher than 1!")  # should above other avg volume

        if parameter_dict['within52w_high_fact'] > 1:
            raise AttributeError("parameter within52w_high_fact must be lower than 1!")  # should above other avg volume

        if not signal_is_volume_high_enough(stock_data_container.historical_stock_data):
            return None

        if not signal_is_volume_raising(stock_data_container.historical_stock_data, parameter_dict['check_days'], parameter_dict['min_cnt'], parameter_dict['min_vol_dev_fact']):
            return None

        if not signal_is52_w_high(stock_data_container.historical_stock_data, parameter_dict['within52w_high_fact']):
            return None

        return stock_data_container
