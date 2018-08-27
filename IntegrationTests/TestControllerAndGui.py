import unittest

import main_v1_support
from GUI.main_v1 import Framework
from Utils.GlobalVariables import *
import ast
from Utils.file_utils import check_file_exists_and_delete
from Strategies.StrategyFactory import StrategyFactory

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk

    py3 = 0
except ImportError:
    import tkinter.ttk as ttk

    py3 = 1

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestControllerAndGui(unittest.TestCase):
    def test_dump_and_load_other_parameter_to_file(self):
        global val, w, root
        root = Tk()
        top = Framework(root)
        controller = main_v1_support.init(root, top)

        strat_param_file = GlobalVariables.get_data_files_path() + '\\TestData\\ParameterFile_test_dump_and_load_strat_params.pickle'
        check_file_exists_and_delete(strat_param_file)

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
        stock_data_file = 'C:\\temp\\pythonFinance\\pythonFinance\\DataFiles\\TestData\\stock_data_container_file.pickle'
        other_params = {'stock_data_container_file': stock_data_file, 'list_with_stock_pages_to_read': {
            'SP500': {'websource_address': "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                      'find_name': 'table', 'class_name': 'class', 'table_class': 'wikitable sortable',
                      'ticker_column_to_read': 0, 'name_column_to_read': 1, 'stock_exchange': 'en'}},
                        'RiskModels': {'FixedSizeRiskModel': {'FixedPositionSize': 2500}}}

        params = {'Strategies': strategy_parameter_dict, 'OtherParameters': other_params}
        req_params = StrategyFactory.get_required_parameters_with_default_parameters()
        controller.dump_analysis_parameters_to_file(strat_param_file, params, req_params)

        controller.load_analysis_parameters_from_file(strat_param_file, req_params)
        self.assertEqual(ast.literal_eval(params), controller.model.analysis_parameters.get(), req_params)

    def test_dump_params(self):
        global val, w, root
        root = Tk()
        top = Framework(root)
        controller = main_v1_support.init(root, top)

        strat_param_file = GlobalVariables.get_data_files_path() + '\\TestData\\ParameterFile_test_dump_and_load_strat_params.pickle'
        check_file_exists_and_delete(strat_param_file)

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
                                                                          'ticker_needed': False}}}
                                   }
        stock_data_file = 'C:\\temp\\pythonFinance\\pythonFinance\\DataFiles\\TestData\\stock_data_container_file.pickle'
        other_params = {'stock_data_container_file': stock_data_file, 'list_with_stock_pages_to_read': {
            'SP500': {'websource_address': "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                      'find_name': 'table', 'class_name': 'class', 'table_class': 'wikitable sortable',
                      'ticker_column_to_read': 0, 'name_column_to_read': 1, 'stock_exchange': 'en'}},
                        'RiskModels': {'FixedSizeRiskModel': {'FixedPositionSize': 2500}}}

        params = {'Strategies': strategy_parameter_dict, 'OtherParameters': other_params}
        req_params = StrategyFactory.get_required_parameters_with_default_parameters()
        import _pickle as pickle
        with open(strat_param_file, "wb") as f:
            pickle.dump(params, f)

        # controller.load_analysis_parameters_from_file(strat_param_file, req_params)
        # self.assertEqual(ast.literal_eval(params), controller.model.get_analysis_parameters(), req_params)
