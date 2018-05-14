from abc import ABC, abstractmethod


class StockDataReader(ABC):
    def __init__(self, period, interval, stock_name, date_time_format):
        self.date_time_format = date_time_format
        self.stock_name = stock_name
        self.interval = interval
        self.period = period

    @abstractmethod
    def read_data(self):
        pass
