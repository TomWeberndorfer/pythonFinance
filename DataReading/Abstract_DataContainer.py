from abc import abstractmethod


class Abstract_DataContainer():

    def __init__(self, stock_name, stock_ticker, stock_exchange):
        self._stock_exchange = stock_exchange
        self._stock_name = stock_name
        self._stock_ticker = stock_ticker
        self._recommendation_strategies = []

    def __str__(self):
        return self._stock_name + ", " + self._stock_ticker

    def __eq__(self, other):
        return other.get_stock_name() == self.get_stock_name() and other.stock_ticker() == self.stock_ticker()

    @abstractmethod
    def get_names_and_values(self):
        raise Exception("Abstractmethod")

    # @property
    def stock_exchange(self):
        return self._stock_exchange

    # @property
    def get_stock_name(self):
        return self._stock_name

    # @property
    def stock_ticker(self):
        return self._stock_ticker

    def get_recommendation_strategies(self):
        return self._recommendation_strategies

    def append_used_strategy(self, strategy_name):
        """
        Append the strategy which where used to get the result.
        :param strategy_name: strategy name as implemented
        :return: nothing
        """
        self.get_recommendation_strategies().append(strategy_name)
