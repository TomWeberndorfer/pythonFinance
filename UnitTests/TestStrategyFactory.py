import unittest

from Strategies.W52HighTechnicalStrategy import W52HighTechnicalStrategy
from Strategies.SimplePatternNewsStrategy import SimplePatternNewsStrategy
from Strategies.StrategyFactory import StrategyFactory
from Utils.GlobalVariables import *

# from directory UnitTests to --> root folder with: ..\\..\\
from Utils.common_utils import have_dicts_same_shape

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestStrategyFactory(unittest.TestCase):

    def test_data_in_dict(self):
        stock_data_file = GlobalVariables.get_data_files_path() + "stock_data_container_file.pickle"
        all_strategy_parameters_dict = {'SimplePatternNewsStrategy': {'news_threshold': 0.7,
                                                                      'german_tagger': 'C:\\temp\\pythonFinance\\pythonFinance\\DataFiles\\nltk_german_classifier_data.pickle',
                                                                      'data_readers': {'TraderfoxNewsDataReader':
                                                                          {
                                                                              'last_date_time_file': 'C:\\temp\\pythonFinance\\pythonFinance\\DataFiles\\TestData\\last_date_time.csv',
                                                                              'german_tagger': 'C:\\temp\\pythonFinance\\pythonFinance\\DataFiles\\nltk_german_classifier_data.pickle',
                                                                              'reload_data': True,
                                                                              'ticker_needed': False},
                                                                          'HistoricalDataReader':
                                                                              {'weeks_delta': 52,
                                                                               'data_source': 'iex',
                                                                               'reload_data': True,
                                                                               'ticker_needed': False}}},
                                        'W52HighTechnicalStrategy':
                                            {'check_days': 7,
                                             'min_cnt': 3,
                                             'min_vol_dev_fact': 1.2,
                                             'within52w_high_fact': 0.98,
                                             'data_readers': {'HistoricalDataReader': {
                                                 'weeks_delta': 52,
                                                 'data_source': 'iex',
                                                 'reload_data': False,
                                                 'ticker_needed': True}}},
                                        'GapUpHighVolumeStrategy': {
                                            'min_gap_factor': 1.03}
                                        }
        other_params = {'stock_data_container_file': stock_data_file, 'list_with_stock_pages_to_read': {
            'SP500': {'websource_address': "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                      'find_name': 'table', 'class_name': 'class', 'table_class': 'wikitable sortable',
                      'ticker_column_to_read': 0, 'name_column_to_read': 1, 'stock_exchange': 'en'}},
                        'RiskModels': {'FixedSizeRiskModel': {'FixedPositionSize': 2500}}}

        backtesting_parameters = {'position_size_percents': 0.2, 'initial_cash': 30000,
                                  'trade_commission_percent': 0.005}

        all_strategy_parameters_dict = {'Strategies': all_strategy_parameters_dict}
        all_strategy_parameters_dict.update({"OtherParameters": other_params})
        all_strategy_parameters_dict.update({"BacktestingParameters": backtesting_parameters})
        req_params = StrategyFactory.get_required_parameters_with_default_parameters()

        self.assertTrue(have_dicts_same_shape(req_params, all_strategy_parameters_dict))

        # key "news" instead of "news_threshold"
        corrupted_strategy_parameter_dict = {'SimplePatternNewsStrategy': {'news': 0.7,
                                                                           'german_tagger': 'C:\\temp\\pythonFinance\\pythonFinance\\DataFiles\\nltk_german_classifier_data.pickle',
                                                                           'data_readers': {'TraderfoxNewsDataReader':
                                                                               {
                                                                                   'last_date_time_file': 'C:\\temp\\pythonFinance\\pythonFinance\\DataFiles\\TestData\\last_date_time.csv',
                                                                                   'german_tagger': 'C:\\temp\\pythonFinance\\pythonFinance\\DataFiles\\nltk_german_classifier_data.pickle',
                                                                                   'reload_data': True,
                                                                                   'ticker_needed': False},
                                                                               'HistoricalDataReader':
                                                                                   {'weeks_delta': 52,
                                                                                    'data_source': 'iex',
                                                                                    'reload_data': True,
                                                                                    'ticker_needed': False}}},
                                             'W52HighTechnicalStrategy':
                                                 {'check_days': 7,
                                                  'min_cnt': 3,
                                                  'min_vol_dev_fact': 1.2,
                                                  'within52w_high_fact': 0.98,
                                                  'data_readers': {'HistoricalDataReader': {
                                                      'weeks_delta': 52,
                                                      'data_source': 'iex',
                                                      'reload_data': False,
                                                      'ticker_needed': True}}}
                                             }

        self.assertFalse(have_dicts_same_shape(req_params, corrupted_strategy_parameter_dict))

        # missing 'SimplePatternNewsStrategy'
        missing_strategy_parameter_dict = {'W52HighTechnicalStrategy':
                                               {'check_days': 7,
                                                'min_cnt': 3,
                                                'min_vol_dev_fact': 1.2,
                                                'within52w_high_fact': 0.98,
                                                'data_readers': {'HistoricalDataReader': {
                                                    'weeks_delta': 52,
                                                    'data_source': 'iex',
                                                    'reload_data': False,
                                                    'ticker_needed': True}}}
                                           }

        self.assertFalse(have_dicts_same_shape(req_params, missing_strategy_parameter_dict))

    def test_partial_data_in_dict(self):
        stock_data_file = GlobalVariables.get_data_files_path() + "stock_data_container_file.pickle"
        req_params = StrategyFactory.get_required_parameters_with_default_parameters()

        missing_strategy_parameter_dict = {'W52HighTechnicalStrategy':
                                               {'check_days': 7,
                                                'min_cnt': 3,
                                                'min_vol_dev_fact': 1.2,
                                                'within52w_high_fact': 0.98,
                                                'data_readers': {'HistoricalDataReader': {
                                                    'weeks_delta': 52,
                                                    'data_source': 'iex',
                                                    'reload_data': False,
                                                    'ticker_needed': True}}}
                                           }

        other_params = {'stock_data_container_file': stock_data_file, 'list_with_stock_pages_to_read': {
            'SP500': {'websource_address': "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                      'find_name': 'table', 'class_name': 'class', 'table_class': 'wikitable sortable',
                      'ticker_column_to_read': 0, 'name_column_to_read': 1, 'stock_exchange': 'en'}},
                        'RiskModels': {'FixedSizeRiskModel': {'FixedPositionSize': 2500}}}

        all_strategy_parameters_dict = {'Strategies': missing_strategy_parameter_dict}
        all_strategy_parameters_dict.update({"OtherParameters": other_params})

        self.assertFalse(have_dicts_same_shape(req_params['Strategies']['W52HighTechnicalStrategy'],
                                               missing_strategy_parameter_dict))
