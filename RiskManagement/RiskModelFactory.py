from DataReading.Abstract_ReaderFactory import Abstract_ReaderFactory
from DataReading.HistoricalDataReaders.HistoricalDataReader import HistoricalDataReader
from DataReading.NewsStockDataReaders.TraderfoxNewsDataReader import TraderfoxNewsDataReader

# todo umstellen auf abstract factory
# https://sourcemaking.com/design_patterns/factory_method
from RiskManagement.Abstract_RiskModelFactory import Abstract_RiskModelFactory
from RiskManagement.FixedSizeRiskModel import FixedSizeRiskModel


class RiskModelFactory(Abstract_RiskModelFactory):

    def _create_risk_model(self, model_to_create, stock_data_container_list, parameter_dict):
        if model_to_create in "FixedSizeRiskModel":
            storage = FixedSizeRiskModel(stock_data_container_list, parameter_dict)

        else:
            raise NotImplementedError

        return storage
