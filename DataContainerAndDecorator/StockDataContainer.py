from DataContainerAndDecorator.Abstract_StockDataContainer import Abstract_DataContainer


class StockDataContainer(Abstract_DataContainer):
    def __init__(self, stock_name, stock_ticker, stock_exchange, historical_stock_data=[], stock_current_prize=0):
        Abstract_DataContainer.__init__(self, stock_name, stock_ticker, stock_exchange)
        self._historical_stock_data = historical_stock_data
        self._stock_current_prize = stock_current_prize

    def get_names_and_values(self):
        """
        Method to return the _names and values as dictionary to insert in a treeview or else.
        :return: a dict with _names as keys and values, Ex: {'Stockname': "Apple Inc."}
        """
        names_and_values_dict = {'Rank': self.get_rank(),
                                 'StrategyAndRecommendation': self.get_recommendation_strategies(),
                                 'Stockname': self.get_stock_name(), "Ticker": self.stock_ticker(),
                                 "Exchange": self.stock_exchange(), 'StopBuy': self.get_stop_buy(),
                                 'StopLoss': self.get_stop_loss(), "Stock Current Prize": self.stock_current_prize(),
                                 'PositionSize': self.get_position_size(),
                                 'RiskModels': self.get_risk_model()}
        return names_and_values_dict

    def historical_stock_data(self):
        return self._historical_stock_data

    def set_historical_stock_data(self, historical_stock_data):
        self._historical_stock_data = historical_stock_data

    def set_stock_current_prize(self, stock_current_prize):
        self._stock_current_prize = stock_current_prize

    def stock_current_prize(self):
        return self._stock_current_prize



