from datetime import datetime
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
        self._stop_buy = 0
        self._stop_loss = 0
        self._position_size = 0

        # TODO does it make sense more than 1 risk model?
        self._risk_model = ''

    def __str__(self):
        return self._stock_name + ", " + self._stock_ticker

    def __eq__(self, other):
        return other.get_stock_name() == self.get_stock_name() and other.stock_ticker() == self.stock_ticker()

    @abstractmethod
    def get_names_and_values(self):
        """
        Method to return the _names and values as dictionary to insert in a treeview or else.
        :return: a dict with _names as keys and values, Ex: {'Stockname': "Apple Inc"}
        """
        raise Exception("Abstractmethod")

    def get_rank(self):
        rank = 0
        for strat in self.get_recommendation_strategies():
            if self.get_recommendation_strategies()[strat][0] is "BUY":
                rank = rank + 1
            else:
                rank = rank - 1
        return rank

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

    def update_used_strategy_and_recommendation(self, strategy_name, recommendation_text):
        """
        Append the strategy which where used to get the result.
        :param recommendation_text: text to insert (BUY / SELL)
        :param strategy_name: strategy name as implemented
        :return: nothing
        """
        self.get_recommendation_strategies().update({strategy_name: [recommendation_text, str(datetime.now())]})

    def set_stop_buy(self, sb):
        self._stop_buy = sb

    def get_stop_buy(self):
        return self._stop_buy

    def set_stop_loss(self, sl):
        self._stop_loss = sl

    def get_stop_loss(self):
        return self._stop_loss

    def set_position_size(self, size):
        self._position_size = size

    def get_position_size(self):
        """
        Position size in units of a stock.
        :return: number of stocks
        """
        return self._position_size

    def get_risk_model(self):
        return self._risk_model

    def set_risk_model(self, risk_model):
        self._risk_model = str(risk_model)
