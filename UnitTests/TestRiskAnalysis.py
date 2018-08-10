import os
import unittest
from pandas import DataFrame, np
from datetime import datetime

from DataReading.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataReading.StockDataContainer import StockDataContainer
from RiskManagement.FixedSizeRiskModel import FixedSizeRiskModel
from RiskManagement.RiskModelFactory import RiskModelFactory
from StockAnalysis import _read_data
from Utils.GlobalVariables import *

# from directory UnitTests to --> root folder with: ..\\..\\
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestRiskAnalysis(unittest.TestCase):
    def test__read_data__TraderfoxNewsDataReader_news_data(self):
        fixes_pos_size = 2500
        strategy_parameter_dict = {'W52HighTechnicalStrategy': {'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2,
                                                                'within52w_high_fact': 0.98, 'data_readers': [
                {'Name': 'HistoricalDataReader', 'weeks_delta': 52, 'data_source': 'iex', 'reload_data': False,
                 'ticker_needed': False}]}}
        stock_data_file = 'C:\\temp\\pythonFinance\\pythonFinance\\DataFiles\\TestData\\stock_data_container_file.pickle'

        # attention these are test data files
        other_params = {
            'stock_data_container_file': 'C:\\temp\\pythonFinance\\pythonFinance\\DataFiles\\TestData\\stock_data_container_file.pickle',
            'list_with_stock_pages_to_read': {
                'SP500': {'websource_address': "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                          'find_name': 'table', 'class_name': 'class', 'table_class': 'wikitable sortable',
                          'ticker_column_to_read': 0, 'name_column_to_read': 1, 'stock_exchange': 'en'}},

            'RiskModels': {'FixedSizeRiskModel': {'FixedPositionSize': fixes_pos_size}}}

        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
            ('2016-10-10', 23.62, 23.88, 23.55, 24.0, 44000),
            ('2016-10-11', 23.62, 30.0, 23.01, 23.16, 45000),
            ('2016-10-12', 23.16, 23.0, 23.11, 23.5, 46000)]

        df = DataFrame.from_records(data, columns=labels)
        stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [stock_data_container]

        risk_models = other_params['RiskModels']
        for rm_name in risk_models.keys():
            rm_parameters = risk_models[rm_name]
            rm_factory = RiskModelFactory()
            fsr = rm_factory.prepare(rm_name, stock_data_container_list, rm_parameters)
            fsr.determine_risk()

        self.assertEqual("FixedSizeRiskModel", stock_data_container_list[0].get_risk_model())

        # real calculation with real 52 w high value
        sb = 30.15
        self.assertEqual(np.math.isclose(stock_data_container_list[0].get_stop_buy(), sb, abs_tol=0.001),
                         True)  # =30*1.005
        self.assertEqual(np.math.isclose(stock_data_container_list[0].get_stop_loss(), 29.25, abs_tol=0.001),
                         True)  # =30*1.005*0.97
        self.assertEqual(
            np.math.isclose(stock_data_container_list[0].get_position_size(), int(fixes_pos_size / sb), abs_tol=0.001),
            True)
