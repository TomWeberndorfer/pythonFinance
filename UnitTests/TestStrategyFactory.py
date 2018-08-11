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

    def test_StockDataContainer_get_required_parameters_with_default_parameters(self):
        req_params = StrategyFactory.get_required_parameters_with_default_parameters()

        w52_params = W52HighTechnicalStrategy.get_required_parameters_with_default_parameters()
        simple_news_params = SimplePatternNewsStrategy.get_required_parameters_with_default_parameters()

        params_dict = {}
        params_dict.update(w52_params)
        params_dict.update(simple_news_params)

        self.assertEqual(params_dict, req_params)

    def test_data_in_dict(self):
        strategy_parameter_dict = {'SimplePatternNewsStrategy': {'news_threshold': 0.7,
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
        req_params = StrategyFactory.get_required_parameters_with_default_parameters()

        self.assertTrue(have_dicts_same_shape(req_params, strategy_parameter_dict))

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
