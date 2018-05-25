import os
import threading
import traceback
from abc import abstractmethod
from datetime import datetime, timedelta

from Strategies.Strategy import strat_scheduler
from Utils.common_utils import split_list, print_stocks_to_buy
from Utils.file_utils import FileUtils, read_tickers_from_file

# TODO übergeben
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class StockScreener():
    def prepare_strategy(self, strategy_to_create, stock_data_container_list, parameter_list):
        strategy = self._create_strategy(strategy_to_create, stock_data_container_list, parameter_list)
        return strategy

    @abstractmethod
    def _create_strategy(self, strategy_to_create):
        raise Exception("Abstractmethod")


