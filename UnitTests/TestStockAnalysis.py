import unittest

from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Utils.StockAnalysis import _read_data
from Utils.GlobalVariables import *

# from directory UnitTests to --> root folder with: ..\\..\\
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestStockAnalysis(unittest.TestCase):
    def test__read_data__HistoricalDataReader__both_container_filled_with_hist_data(self):
        ticker_needed = False
        data_file_path = GlobalVariables.get_data_files_path()
        strategy_parameter_dict = {'W52HighTechnicalStrategy': {'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2,
                                                                'within52w_high_fact': 0.98,
                                                                'data_readers': {
                                                                    'HistoricalDataReader': {'weeks_delta': 52,
                                                                                             'data_source': 'iex',
                                                                                             'reload_data': False,
                                                                                             'ticker_needed': ticker_needed}}}}
        stock_data_file = data_file_path + 'TestData\\stock_data_container_file.pickle'
        other_params = {'stock_data_container_file': stock_data_file, 'dict_with_stock_pages_to_read': {
            'SP500': {'websource_address': "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                      'find_name': 'table', 'class_name': 'class', 'table_class': 'wikitable sortable',
                      'ticker_column_to_read': 0, 'name_column_to_read': 1, 'stock_exchange': 'en'}},
                        'RiskModels': {
                            'FixedSizeRiskModel': {'OrderTarget': 'order_target_value', 'TargetValue': 2500}}}

        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)

        apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        intel_container = StockDataContainer("Intel Corporation", "INTC", "")
        stock_data_container_list = [apple_stock_data_container, intel_container]

        stock_data_container_list = _read_data(['W52HighTechnicalStrategy'], strategy_parameter_dict, other_params,
                                               stock_data_container_list)

        apple_idx = stock_data_container_list.index(apple_stock_data_container)
        intel_idx = stock_data_container_list.index(intel_container)
        self.assertEqual(len(stock_data_container_list), 2)
        self.assertEqual(stock_data_container_list[apple_idx].get_stock_name(), "Apple Inc.")
        self.assertEqual(stock_data_container_list[intel_idx].get_stock_name(), "Intel Corporation")
        self.assertGreater(len(stock_data_container_list[apple_idx].historical_stock_data()), 200)
        self.assertGreater(len(stock_data_container_list[intel_idx].historical_stock_data()), 200)
        self.assertNotEqual(
            stock_data_container_list[apple_idx].historical_stock_data()[GlobalVariables.get_stock_data_labels_dict()['High']][
                0],
            stock_data_container_list[0].historical_stock_data()[GlobalVariables.get_stock_data_labels_dict()['High']][
                intel_idx])

    def test__read_data__TraderfoxNewsDataReader_historical_data__both_container_filled_with_hist_data(self):
        # attention these are test data files
        data_file_path = GlobalVariables.get_data_files_path()
        strategy_parameter_dict = {'SimplePatternNewsStrategy': {'news_threshold': 0.7,
                                                                 'german_tagger': data_file_path + 'nltk_german_classifier_data.pickle',
                                                                 'data_readers': {'TraderfoxNewsDataReader':
                                                                     {
                                                                         'last_check_date_file': data_file_path + 'TestData\\last_date_time.csv',
                                                                         'german_tagger': data_file_path + 'nltk_german_classifier_data.pickle',
                                                                         'reload_data': True,
                                                                         'ticker_needed': False},
                                                                     'HistoricalDataReader': {
                                                                         'weeks_delta': 52,
                                                                         'data_source': 'iex',
                                                                         'reload_data': True,
                                                                         'ticker_needed': False}
                                                                 }
                                                                 }
                                   }
        stock_data_file = data_file_path + 'TestData\\stock_data_container_file.pickle'
        other_params = {'stock_data_container_file': stock_data_file, 'dict_with_stock_pages_to_read': {
            'SP500': {'websource_address': "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                      'find_name': 'table', 'class_name': 'class', 'table_class': 'wikitable sortable',
                      'ticker_column_to_read': 0, 'name_column_to_read': 1, 'stock_exchange': 'en'}},
                        'RiskModels': {
                            'FixedSizeRiskModel': {'OrderTarget': 'order_target_value', 'TargetValue': 2500}}}

        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)

        apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        intel_container = StockDataContainer("Intel Corporation", "INTC", "")
        stock_data_container_list = [apple_stock_data_container, intel_container]

        stock_data_container_list = _read_data(['SimplePatternNewsStrategy'], strategy_parameter_dict, other_params,
                                               stock_data_container_list)

        apple_idx = stock_data_container_list.index(apple_stock_data_container)
        intel_idx = stock_data_container_list.index(intel_container)
        self.assertGreater(len(stock_data_container_list), 2)
        self.assertEqual(stock_data_container_list[apple_idx].get_stock_name(), "Apple Inc.")
        self.assertEqual(stock_data_container_list[intel_idx].get_stock_name(), "Intel Corporation")
        self.assertGreater(len(stock_data_container_list[apple_idx].historical_stock_data()), 200)
        self.assertGreater(len(stock_data_container_list[intel_idx].historical_stock_data()), 200)
        self.assertNotEqual(
            stock_data_container_list[apple_idx].historical_stock_data()[GlobalVariables.get_stock_data_labels_dict()['High']][
                0],
            stock_data_container_list[0].historical_stock_data()[GlobalVariables.get_stock_data_labels_dict()['High']][
                intel_idx])

    def test__read_data__TraderfoxNewsDataReader_news_data(self):
        # attention these are test data files
        data_file_path = GlobalVariables.get_data_files_path()
        strategy_parameter_dict = {'SimplePatternNewsStrategy': {'news_threshold': 0.7,
                                                                 'german_tagger': data_file_path + 'nltk_german_classifier_data.pickle',
                                                                 'data_readers': {'TraderfoxNewsDataReader':
                                                                     {
                                                                         'last_check_date_file': data_file_path + 'TestData\\last_date_time.csv',
                                                                         'german_tagger': data_file_path + 'nltk_german_classifier_data.pickle',
                                                                         'reload_data': True,
                                                                         'ticker_needed': False},
                                                                     'HistoricalDataReader':
                                                                         {'weeks_delta': 52,
                                                                          'data_source': 'iex',
                                                                          'reload_data': True,
                                                                          'ticker_needed': False}}}}
        stock_data_file = data_file_path + 'TestData\\stock_data_container_file.pickle'
        other_params = {'stock_data_container_file': stock_data_file, 'dict_with_stock_pages_to_read': {
            'SP500': {'websource_address': "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                      'find_name': 'table', 'class_name': 'class', 'table_class': 'wikitable sortable',
                      'ticker_column_to_read': 0, 'name_column_to_read': 1, 'stock_exchange': 'en'}},
                        'RiskModels': {
                            'FixedSizeRiskModel': {'OrderTarget': 'order_target_value', 'TargetValue': 2500}}}
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)

        stock_data_container_list = []
        stock_data_container_list = _read_data(['SimplePatternNewsStrategy'], strategy_parameter_dict, other_params,
                                               stock_data_container_list)

        self.assertGreater(len(stock_data_container_list), 2)
        self.assertGreater(len(stock_data_container_list[0].original_news()), 10)
        self.assertGreater(len(stock_data_container_list[2].original_news()), 10)
