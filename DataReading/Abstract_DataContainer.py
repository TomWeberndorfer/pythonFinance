from abc import abstractmethod


class Abstract_DataContainer:

    def __init__(self, stock_name, stock_ticker, stock_exchange):
        """
        Init the data container with given parameters
        :param stock_name: full name of the stock
        :param stock_ticker: short ticker of the stock (Apple Inc. --> AAPL)
        :param stock_exchange: stock exchange (Börse) to trade
        """
        self._stock_exchange = stock_exchange
        self._stock_name = stock_name
        self._stock_ticker = stock_ticker
        self._strategy_and_recommendation = {}

    def __str__(self):
        return self._stock_name + ", " + self._stock_ticker

    def __eq__(self, other):
        return other.get_stock_name() == self.get_stock_name() and other.stock_ticker() == self.stock_ticker()

    @abstractmethod
    def get_names_and_values(self):
        """
        Method to return the names and values as dictionary to insert in a treeview or else.
        :return: a dict with names as keys and values, Ex: {'Stockname': "Apple Inc"}
        """
        raise Exception("Abstractmethod")

    def get_rank(self):
        return len(self.get_recommendation_strategies())

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
        return self._strategy_and_recommendation

    def updated_used_strategy_and_recommendation(self, strategy_name, recommendation_text):
        """
        Append the strategy which where used to get the result.
        :param strategy_name: strategy name as implemented
        :return: nothing
        """
        self.get_recommendation_strategies().update({strategy_name: recommendation_text})
