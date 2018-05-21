from abc import ABC, abstractmethod


class StockDataReader(ABC):

    @abstractmethod
    def read_data(self):
        pass
