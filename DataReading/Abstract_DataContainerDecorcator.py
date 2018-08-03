from abc import abstractmethod

from DataReading.Abstract_DataContainer import Abstract_DataContainer


class Abstract_DataContainerDecorator(Abstract_DataContainer):

    def __init__(self, shaped_data_container):
        self._shaped_data_container = shaped_data_container

    @abstractmethod
    def get_names_and_values(self):
        """
        Method to return the _names and values as dictionary to insert in a treeview or else.
        Should also return the data from the wrapped shaped data container
        :return: a dict with _names as keys and values, Ex: {'Stockname': "Apple Inc"}
        """
        self._shaped_data_container.get_names_and_values()

    def stock_exchange(self):
        return self._shaped_data_container.stock_exchange()

    def get_stock_name(self):
        return self._shaped_data_container.get_stock_name()

    def stock_ticker(self):
        return self._shaped_data_container.stock_ticker()

    #TODO 11: i wills eig ned in den wrapper
    def get_recommendation_strategies(self):
        return self._shaped_data_container.get_recommendation_strategies()

    def set_stop_buy(self, sb):
        self._shaped_data_container._stop_buy = sb

    def get_stop_buy(self):
        return self._shaped_data_container._stop_buy

    def set_stop_loss(self, sl):
        self._shaped_data_container._stop_loss = sl

    def get_stop_loss(self):
        return self._shaped_data_container._stop_loss

    def set_position_size(self, size):
        self._shaped_data_container._position_size = size

    def get_position_size(self):
        return self._shaped_data_container._position_size

    def historical_stock_data(self):
        return self._shaped_data_container._historical_stock_data

    def get_risk_model(self):
        self._shaped_data_container._risk_model

    def set_risk_model(self, risk_model):
        self._shaped_data_container._risk_model = str(risk_model)

    def set_historical_stock_data(self, historical_stock_data_df):
        self._shaped_data_container.set_historical_stock_data(historical_stock_data_df)

    def get_historical_stock_data(self):
        return self._shaped_data_container.get_historical_stock_data()
