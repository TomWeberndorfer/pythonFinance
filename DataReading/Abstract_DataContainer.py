from abc import abstractmethod


class Abstract_DataContainer():
    def __str__(self):
        return self.stock_name + ", " + self.stock_ticker

    def __eq__(self, other):
        return other.stock_name == self.stock_name and other.stock_ticker == self.stock_ticker

    @abstractmethod
    def get_names_and_values(self):
        raise Exception("Abstractmethod")
