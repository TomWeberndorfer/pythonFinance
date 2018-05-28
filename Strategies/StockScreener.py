import os
from abc import abstractmethod

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


