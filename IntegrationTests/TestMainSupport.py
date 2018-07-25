import os
import unittest

import time
from pandas import DataFrame

import main_v1_support
from DataReading.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataReading.StockDataContainer import StockDataContainer
from GUI.main_v1 import ScrolledTreeView, LabelFrame, vp_start_gui, Framework
from MvcModel import MvcModel
from Utils.GuiUtils import GuiUtils
from Utils.GlobalVariables import *
from threading import Thread

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

        controller.load_other_parameter_from_file(
            GlobalVariables.get_data_files_path() + '\\TestData\\OtherParameterFile_DO_NOT_RELOAD.pickle')
        controller.load_strategy_parameter_from_file(
            GlobalVariables.get_data_files_path() + '\\TestData\\ParameterFile_test_strategy_w52.pickle')
        controller.model.set_strategy_selection_value(['W52HighTechnicalStrategy'])
        root.mainloop()

        result_container = controller.model.get_result_stock_data_container_list()

        print(str(result_container))
        self.assertEqual(3, len(result_container))
        self.assertEqual('CSX Corp.', result_container[0].get_stock_name())
        self.assertEqual('Microsoft Corp.', result_container[1].get_stock_name())
        self.assertEqual('V.F. Corp.', result_container[2].get_stock_name())

        # self.assertEqual(["{}", "test1", "t1", "en", "{}", "test2", "t2", "de"], result_values)
