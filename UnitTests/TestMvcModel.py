import unittest

import main_v1_support
from GUI.ScrollableFrame import ScrollableFrame
from Utils.GlobalVariables import *

# from directory UnitTests to --> root folder with: ..\\..\\
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'
from GUI.main_v1 import vp_start_gui, Framework, create_Framework
from MvcModel import MvcModel
from Utils.GlobalVariables import *
from Utils.file_utils import check_file_exists_and_delete

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


class TestMvcModel(unittest.TestCase):
    def test_update_column_list__add_several_columns__add_redundant_columns(self):
        model = MvcModel(None)
        self.assertEqual([], model.get_column_list())

        columns_to_add = ['StrategyAndRecommendation', 'Stockname']
        is_updated = model.update_column_list(columns_to_add)
        self.assertTrue(is_updated)
        self.assertEqual(columns_to_add, model.get_column_list())

        columns_to_add_2 = ["Ticker", "Exchange"]
        is_updated = model.update_column_list(columns_to_add_2)
        self.assertTrue(is_updated)
        cols = columns_to_add
        cols.extend(columns_to_add_2)
        self.assertEqual(cols, model.get_column_list())

        # redundant columns should not be added again
        redundant_cols = ['Stockname', "Ticker"]
        is_updated = model.update_column_list(redundant_cols)
        self.assertFalse(is_updated)
        self.assertEqual(cols, model.get_column_list())

    def test_add_to_other_params(self):
        root = Tk()
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

        sf = ScrollableFrame(root)
        sf.populateFormParameters(params)
        form = sf.form
        at = form.at
        at_objects = form.at_objects

        my_col_2, my_row, all_txt = form._read_objects_as_dict_recursive(at_objects, 0, 0)

        self.assertEqual(params, at)
        self.assertEqual(params, all_txt)

        all_txt = form.get_parameters(at_objects)
        self.assertEqual(params, all_txt)
