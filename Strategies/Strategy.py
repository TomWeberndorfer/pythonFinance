from abc import ABC, abstractmethod


class Strategy(ABC):
    def __init__(self, stock_name_list, stock_data_list, parameter_list, stocks_to_buy):
        self.stocks_to_buy = stocks_to_buy
        self.parameter_list = parameter_list
        self.stock_data_list = stock_data_list
        self.stock_name_list = stock_name_list
        super().__init__()

    @abstractmethod
    def create_strategy(self):
        pass
