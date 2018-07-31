import os
import unittest
from pandas import DataFrame, np
from datetime import datetime

from DataReading.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataReading.StockDataContainer import StockDataContainer
from RiskManagement.FixedSizeRiskModel import FixedSizeRiskModel
from Utils.GlobalVariables import *

# from directory UnitTests to --> root folder with: ..\\..\\
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestFixedSizeRiskModel(unittest.TestCase):
    def test_TestFixedSizeRiskModel(self):
        parameter_dict = {'FixedPositionSize': 2500}

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
        stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [stock_data_container]

        fsr = FixedSizeRiskModel(stock_data_container_list, parameter_dict)
        fsr.determine_risk()

        self.assertEqual(np.math.isclose(26.130, stock_data_container_list[0].get_stop_buy(), abs_tol=0.01), True)
        self.assertEqual(np.math.isclose(25.35, stock_data_container_list[0].get_stop_loss(), abs_tol=0.01), True)
        self.assertEqual(np.math.isclose(95, stock_data_container_list[0].get_position_size(), abs_tol=0.01), True)
