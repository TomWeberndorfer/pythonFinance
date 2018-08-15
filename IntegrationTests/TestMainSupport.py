import os
import unittest

import time
from pandas import DataFrame

import main_v1_support
from DataReading.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataReading.StockDataContainer import StockDataContainer
from GUI.main_v1 import ScrolledTreeView, LabelFrame, vp_start_gui
from MvcModel import MvcModel
from Utils.GuiUtils import GuiUtils
from Utils.GlobalVariables import *
from threading import Thread
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


class TestMainSupport(unittest.TestCase):
    def test_stock_data_container_file__W52HighTechnicalStrategy_msft_vfc_csx(self):
        raise Exception("This test is not working ")
        global val, w, root
        root = Tk()
        top = Framework(root)
        controller = main_v1_support.init(root, top)

        req_params = StrategyFactory.get_required_parameters_with_default_parameters()

        controller.load_analysis_parameters_from_file(
            GlobalVariables.get_data_files_path() + '\\TestData\\OtherParameterFile_DO_NOT_RELOAD.pickle', req_params)
        controller.model.strategy_selection_values.set(['W52HighTechnicalStrategy'])
        root.mainloop()

        result_container = controller.model.result_stock_data_container_list.get()

        print(str(result_container))
        self.assertEqual(3, len(result_container))
        self.assertEqual('CSX Corp.', result_container[0].get_stock_name())
        self.assertEqual('Microsoft Corp.', result_container[1].get_stock_name())
        self.assertEqual('V.F. Corp.', result_container[2].get_stock_name())

        # self.assertEqual(["{}", "test1", "t1", "en", "{}", "test2", "t2", "de"], result_values)
