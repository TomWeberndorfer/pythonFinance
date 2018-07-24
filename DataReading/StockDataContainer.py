from DataReading.Abstract_DataContainer import Abstract_DataContainer


class StockDataContainer(Abstract_DataContainer):
    def __init__(self, stock_name, stock_ticker, stock_exchange, historical_stock_data=[], stock_current_prize=0):
        Abstract_DataContainer.__init__(self, stock_name, stock_ticker, stock_exchange)
        self._historical_stock_data = historical_stock_data
        self._stock_current_prize = stock_current_prize

    def get_names_and_values(self):
        """
        Method to return the names and values as dictionary to insert in a treeview or else.
        :return: a dict with names as keys and values, Ex: {'Stockname': "Apple Inc"}
        """
        names_and_values_dict = {'StrategyAndRecommendation': self.get_recommendation_strategies(),
                                 'Stockname': self.get_stock_name(), "Ticker": self.stock_ticker(),
                                 "Exchange": self.stock_exchange()}
        return names_and_values_dict

    def historical_stock_data(self):
        return self._historical_stock_data

    def set_historical_stock_data(self, historical_stock_data):
        self._historical_stock_data = historical_stock_data

    def set_stock_current_prize(self, stock_current_prize):
        self._stock_current_prize = stock_current_prize

    def stock_current_prize(self):
        return self._stock_current_prize



