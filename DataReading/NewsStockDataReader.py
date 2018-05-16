from abc import ABC, abstractmethod


class NewsStockDataReader(ABC):

    @abstractmethod
    def read_data(self):
        pass
