import unittest

from Strategies.Abstract_Strategy import Abstract_Strategy
from Strategies.StrategyFactory import StrategyFactory
from Utils.GlobalVariables import *
from pandas import DataFrame
# from directory UnitTests to --> root folder with: ..\\..\\
from Utils.CommonUtils import CommonUtils
from DataContainerAndDecorator.StockDataContainer import StockDataContainer

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestStrategyFactory(unittest.TestCase):

    def test_data_in_dict(self):
        stock_data_file = GlobalVariables.get_data_files_path() + "stock_data_container_file.pickle"
        all_strategy_parameters_dict = {'SimplePatternNewsStrategy': {'news_threshold': 0.7,
                                                                      'german_tagger': GlobalVariables.get_data_files_path() + 'nltk_german_classifier_data.pickle',
                                                                      'data_readers': {'TraderfoxNewsDataReader':
                                                                          {
                                                                              'last_check_date_file': GlobalVariables.get_data_files_path() + 'TestData\\last_date_time.csv',
                                                                              'german_tagger': GlobalVariables.get_data_files_path() + 'nltk_german_classifier_data.pickle',
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
        other_params = {'stock_data_container_file': stock_data_file,
                        'dict_with_stock_pages_to_read': {
                            'SP500': {'websource_address': "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                                      'find_name': 'table', 'class_name': 'class', 'table_class': 'wikitable sortable',
                                      'ticker_column_to_read': 0, 'name_column_to_read': 1, 'stock_exchange': 'en'},
                            'DAX': {
                                'websource_address': "http://topforeignstocks.com/stock-lists/the-list-of-listed-companies-in-germany/",
                                'find_name': 'tbody', 'class_name': 'class', 'table_class': 'row-hover',
                                'ticker_column_to_read': 2, 'name_column_to_read': 1, 'stock_exchange': 'de'}},
                        'RiskModels': {
                            'FixedSizeRiskModel': {'OrderTarget': 'order_target_value', 'TargetValue': 2500}},
                        'AutoTrading': {
                            'RepetitiveScreeningInterval': 120,
                            'MaxNumberOfDifferentStocksToBuyPerAutoTrade': 5},
                        'Broker': {
                            'Name': 'IBPyInteractiveBrokers'}
                        }

        backtesting_parameters = {'BacktestingFramework': 'BacktraderWrapper', 'initial_cash': 30000,
                                  'trade_commission_percent': 0.005}

        all_strategy_parameters_dict = {'Strategies': all_strategy_parameters_dict}
        all_strategy_parameters_dict.update({"OtherParameters": other_params})
        all_strategy_parameters_dict.update({"BacktestingParameters": backtesting_parameters})
        req_params = StrategyFactory.get_required_parameters_with_default_parameters()

        self.assertTrue(CommonUtils.have_dicts_same_shape(req_params, all_strategy_parameters_dict))

        # key "news" instead of "news_threshold"
        corrupted_strategy_parameter_dict = {'SimplePatternNewsStrategy': {'news': 0.7,
                                                                           'german_tagger': GlobalVariables.get_data_files_path() + 'nltk_german_classifier_data.pickle',
                                                                           'data_readers': {'TraderfoxNewsDataReader':
                                                                               {
                                                                                   'last_check_date_file': GlobalVariables.get_data_files_path() + 'TestData\\last_date_time.csv',
                                                                                   'german_tagger': GlobalVariables.get_data_files_path() + 'nltk_german_classifier_data.pickle',
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

        self.assertFalse(CommonUtils.have_dicts_same_shape(req_params, corrupted_strategy_parameter_dict))

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

        self.assertFalse(CommonUtils.have_dicts_same_shape(req_params, missing_strategy_parameter_dict))

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

        other_params = {'stock_data_container_file': stock_data_file, 'dict_with_stock_pages_to_read': {
            'SP500': {'websource_address': "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                      'find_name': 'table', 'class_name': 'class', 'table_class': 'wikitable sortable',
                      'ticker_column_to_read': 0, 'name_column_to_read': 1, 'stock_exchange': 'en'}},
                        'RiskModels': {
                            'FixedSizeRiskModel': {'OrderTarget': 'order_target_value', 'TargetValue': 2500}}}

        all_strategy_parameters_dict = {'Strategies': missing_strategy_parameter_dict}
        all_strategy_parameters_dict.update({"OtherParameters": other_params})

        self.assertFalse(CommonUtils.have_dicts_same_shape(req_params['Strategies']['W52HighTechnicalStrategy'],
                                                           missing_strategy_parameter_dict))

    def test_get_implemented_strategies_list(self):
        w52hi_parameter_dict = {'check_days': 5, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98}

        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [('2016-09-30', 23.35, 23.91, 23.24, 23.8, 31000), ]

        df = DataFrame.from_records(data, columns=labels)
        stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [stock_data_container]

        ##################################################
        # 52 w strategy
        stock_screener = StrategyFactory()
        w52_hi_strat = stock_screener.prepare("W52HighTechnicalStrategy",
                                              stock_data_container_list=stock_data_container_list,
                                              analysis_parameters=w52hi_parameter_dict)

        self.assertNotEqual(None, w52_hi_strat)
        self.assertTrue(isinstance(w52_hi_strat, Abstract_Strategy))
