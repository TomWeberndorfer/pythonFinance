import unittest

from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from GUI.main_v1 import ScrolledTreeView, LabelFrame
from Utils.GlobalVariables import *
from Utils.GuiUtils import GuiUtils

# from directory UnitTests to --> root folder with: ..\\..\\
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestGuiUtils(unittest.TestCase):
    def test_insert_into_treeview(self):
        container = StockDataContainer("test1", "t1", "en")
        result_container = container.get_names_and_values()
        self.Labelframe1 = LabelFrame()
        scrolled_treeview1 = ScrolledTreeView(self.Labelframe1)
        existing_columns = ['Rank', 'StrategyAndRecommendation', 'Stockname', "Ticker", "Exchange"]
        GuiUtils.insert_into_treeview(scrolled_treeview1, existing_columns, result_container)

        result_values = []
        for child in scrolled_treeview1.get_children():
            result_values.extend(scrolled_treeview1.item(child)["values"])

        self.assertEqual([0, '{}', 'test1', 't1', 'en', 0, 0, 0, 0, ''], result_values)

        # ---------
        container = StockDataContainer("test1", "t1", "en")
        result_container = container.get_names_and_values()
        self.Labelframe1 = LabelFrame()
        scrolled_treeview1 = ScrolledTreeView(self.Labelframe1)
        existing_columns = ['Rank', 'StrategyAndRecommendation', 'Stockname', "Ticker"]
        GuiUtils.insert_into_treeview(scrolled_treeview1, existing_columns, result_container)

        result_values = []
        for child in scrolled_treeview1.get_children():
            result_values.extend(scrolled_treeview1.item(child)["values"])

        self.assertEqual([0, '{}', 'test1', 't1', 'en', 0, 0, 0, 0, ''], result_values)

        # --------
        container = StockDataContainer("test1", "t1", "en")
        result_container = container.get_names_and_values()
        self.Labelframe1 = LabelFrame()
        scrolled_treeview1 = ScrolledTreeView(self.Labelframe1)
        existing_columns = ['Rank', 'StrategyAndRecommendation', 'Stockname', "Ticker", "Exchange", "TEST"]
        GuiUtils.insert_into_treeview(scrolled_treeview1, existing_columns, result_container)

        result_values = []
        for child in scrolled_treeview1.get_children():
            result_values.extend(scrolled_treeview1.item(child)["values"])

        self.assertEqual([0, '{}', 'test1', 't1', 'en', '-', 0, 0, 0, 0, ''], result_values)

    def test_insert_into_treeview__two_stocks(self):
        self.Labelframe1 = LabelFrame()
        scrolled_treeview1 = ScrolledTreeView(self.Labelframe1)
        existing_columns = ['Rank', 'StrategyAndRecommendation', 'Stockname', "Ticker", "Exchange"]
        container = StockDataContainer("test1", "t1", "en")
        result_container = container.get_names_and_values()
        GuiUtils.insert_into_treeview(scrolled_treeview1, existing_columns, result_container)

        container_stock_2 = StockDataContainer("test2", "t2", "de")
        result_container = container_stock_2.get_names_and_values()
        GuiUtils.insert_into_treeview(scrolled_treeview1, existing_columns, result_container)

        result_values = []
        for child in scrolled_treeview1.get_children():
            result_values.extend(scrolled_treeview1.item(child)["values"])

        self.assertEqual([0, '{}', 'test1', 't1', 'en', 0, 0, 0, 0, '', 0, '{}', 'test2', 't2', 'de', 0, 0, 0, 0, ''],
                         result_values)
