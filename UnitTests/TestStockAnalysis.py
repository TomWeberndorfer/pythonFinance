import unittest

from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Utils.StockAnalysis import _read_data, run_analysis
from Utils.GlobalVariables import *
from pandas import DataFrame

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
            stock_data_container_list[apple_idx].historical_stock_data()[
                GlobalVariables.get_stock_data_labels_dict()['High']][
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
            stock_data_container_list[apple_idx].historical_stock_data()[
                GlobalVariables.get_stock_data_labels_dict()['High']][
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

    ###############################################################################
    def test__read_data__HistoricalDataReader_and_TraderfoxNewsDataReader(self):
        ticker_needed = False
        data_file_path = GlobalVariables.get_data_files_path()
        strategy_parameter_dict = {'W52HighTechnicalStrategy': {'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2,
                                                                'within52w_high_fact': 0.98,
                                                                'data_readers': {
                                                                    'HistoricalDataReader': {'weeks_delta': 52,
                                                                                             'data_source': 'iex',
                                                                                             'reload_data': False,
                                                                                             'ticker_needed': ticker_needed}}},
                                   'SimplePatternNewsStrategy': {'news_threshold': 0.7,
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

        stock_data_container_list = _read_data(['SimplePatternNewsStrategy', 'W52HighTechnicalStrategy'],
                                               strategy_parameter_dict, other_params,
                                               stock_data_container_list)

        apple_idx = stock_data_container_list.index(apple_stock_data_container)
        intel_idx = stock_data_container_list.index(intel_container)
        self.assertGreater(len(stock_data_container_list), 2)
        self.assertEqual(stock_data_container_list[apple_idx].get_stock_name(), "Apple Inc.")
        self.assertEqual(stock_data_container_list[intel_idx].get_stock_name(), "Intel Corporation")
        self.assertGreater(len(stock_data_container_list[apple_idx].historical_stock_data()), 200)
        self.assertGreater(len(stock_data_container_list[intel_idx].historical_stock_data()), 200)
        self.assertNotEqual(
            stock_data_container_list[apple_idx].historical_stock_data()[
                GlobalVariables.get_stock_data_labels_dict()['High']][
                0],
            stock_data_container_list[0].historical_stock_data()[GlobalVariables.get_stock_data_labels_dict()['High']][
                intel_idx])

    # --------------------------------------------------------------------------------------------------------
    def test__run_analysis__HistoricalDataReader(self):
        ticker_needed = False
        data_file_path = GlobalVariables.get_data_files_path()
        strategy_parameter_dict = {'W52HighTechnicalStrategy': {'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2,
                                                                'within52w_high_fact': 0.98,
                                                                'data_readers': {
                                                                    'HistoricalDataReader': {'weeks_delta': 52,
                                                                                             'data_source': 'iex',
                                                                                             'reload_data': True,
                                                                                             'ticker_needed': ticker_needed}}}
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
        data = [('2016-09-30', 23.35, 23.91, 23.24, 23.8, 31000),
                ('2016-10-03', 23.68, 23.69, 23.39, 23.5, 31000),
                ('2016-10-04', 23.52, 23.64, 23.18, 23.28, 31000),
                ('2016-10-05', 23.28, 23.51, 23.27, 23.43, 31000),
                ('2016-10-06', 23.38, 23.56, 23.29, 23.48, 42000),
                ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
                ('2016-10-10', 23.62, 23.88, 23.55, 23.77, 44000),
                ('2016-10-11', 23.62, 23.74, 23.01, 23.16, 45000),
                ('2016-10-12', 23.16, 26, 23.11, 23.18, 46000)]

        df = DataFrame.from_records(data, columns=labels)
        apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        apple_stock_data_container.set_historical_stock_data(df)
        intel_container = StockDataContainer("Intel Corporation", "INTC", "")
        stock_data_container_list = [apple_stock_data_container, intel_container]

        result_analysis = run_analysis(['W52HighTechnicalStrategy'],
                                       strategy_parameter_dict, other_params, stock_data_container_list)

        apple_idx = result_analysis.index(apple_stock_data_container)
        self.assertEqual(result_analysis[apple_idx].get_stock_name(), "Apple Inc.")
        self.assertEqual(len(data), len(result_analysis[apple_idx].historical_stock_data()))
        self.assertEqual(1, len(result_analysis))

    def test__run_analysis__HistoricalDataReader_and_TraderfoxNewsDataReader(self):
        ticker_needed = False
        data_file_path = GlobalVariables.get_data_files_path()
        strategy_parameter_dict = {'SimplePatternNewsStrategy': {'news_threshold': 0.7,
                                                                 'german_tagger': data_file_path + 'nltk_german_classifier_data.pickle',
                                                                 'data_readers': {'TraderfoxNewsDataReader':
                                                                     {
                                                                         'last_check_date_file': data_file_path + 'TestData\\last_date_time.csv',
                                                                         'german_tagger': data_file_path + 'nltk_german_classifier_data.pickle',
                                                                         'reload_data': True,
                                                                         'ticker_needed': ticker_needed},
                                                                     'HistoricalDataReader': {
                                                                         'weeks_delta': 52,
                                                                         'data_source': 'iex',
                                                                         'reload_data': False,
                                                                         'ticker_needed': ticker_needed}
                                                                 }
                                                                 },
                                   'W52HighTechnicalStrategy': {'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2,
                                                                'within52w_high_fact': 0.98,
                                                                'data_readers': {
                                                                    'HistoricalDataReader': {'weeks_delta': 52,
                                                                                             'data_source': 'iex',
                                                                                             'reload_data': True,
                                                                                             'ticker_needed': False}}}
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
        data = [('2016-09-30', 23.35, 23.91, 23.24, 23.8, 31000),
                ('2016-10-03', 23.68, 23.69, 23.39, 23.5, 31000),
                ('2016-10-04', 23.52, 23.64, 23.18, 23.28, 31000),
                ('2016-10-05', 23.28, 23.51, 23.27, 23.43, 31000),
                ('2016-10-06', 23.38, 23.56, 23.29, 23.48, 42000),
                ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
                ('2016-10-10', 23.62, 23.88, 23.55, 23.77, 44000),
                ('2016-10-11', 23.62, 23.74, 23.01, 23.16, 45000),
                ('2016-10-12', 23.16, 26, 23.11, 23.18, 46000)]

        df = DataFrame.from_records(data, columns=labels)
        apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        apple_stock_data_container.set_historical_stock_data(df)
        intel_container = StockDataContainer("Intel Corporation", "INTC", "")
        intel_container.set_historical_stock_data(df)
        stock_data_container_list = [apple_stock_data_container, intel_container]

        # TODO de container müssen technische daten enthalten die 52 w haben, drüfen aber ned überschrieden werden durch lesen
        # --> bast, aber des wird trotzdem ned gemacht, nur wenn 'reload_data': False
        stock_data_container_list = _read_data(['SimplePatternNewsStrategy', 'W52HighTechnicalStrategy'],
                                               strategy_parameter_dict, other_params,
                                               stock_data_container_list)

        result_analysis = run_analysis(['SimplePatternNewsStrategy', 'W52HighTechnicalStrategy'],
                                       strategy_parameter_dict, other_params, stock_data_container_list)

        apple_idx = result_analysis.index(apple_stock_data_container)
        intel_idx = result_analysis.index(intel_container)
        self.assertGreater(len(result_analysis), 2)
        self.assertEqual(result_analysis[apple_idx].get_stock_name(), "Apple Inc.")
        self.assertEqual(result_analysis[intel_idx].get_stock_name(), "Intel Corporation")
        self.assertEqual(len(result_analysis[apple_idx].historical_stock_data()), 9)
        self.assertEqual(len(result_analysis[intel_idx].historical_stock_data()), 9)
