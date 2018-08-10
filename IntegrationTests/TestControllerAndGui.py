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
import ast
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

        content = "{'Test': 2, 'Var2': False}"
        controller.dump_other_parameter_to_file(strat_param_file, content)

        controller.load_other_parameter_from_file(strat_param_file)
        self.assertEqual(ast.literal_eval(content), controller.model.get_other_params())
