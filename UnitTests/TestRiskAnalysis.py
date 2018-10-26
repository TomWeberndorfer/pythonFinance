import unittest
from pandas import DataFrame, np

from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from RiskManagement.RiskModelFactory import RiskModelFactory
from Strategies.StrategyFactory import StrategyFactory
from Utils.GlobalVariables import *

# from directory UnitTests to --> root folder with: ..\\..\\
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestRiskAnalysis(unittest.TestCase):
    def test_RiskModelFactory_and_risk_determinitation(self):
        fixes_pos_size = 2500
        # attention these are test data files
        other_params = GlobalVariables.get_other_parameters_with_default_parameters()

        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)

        calc_val = 23.5  # last high value
        data = [
            ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
            ('2016-10-10', 23.62, 23.88, 23.55, 24.0, 44000),
            ('2016-10-11', 23.62, 30.0, 23.01, 23.16, 45000),
            ('2016-10-12', 23.16, calc_val, 23.11, 23.5, 46000)]

        df = DataFrame.from_records(data, columns=labels)
        stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [stock_data_container]

        risk_models = other_params['RiskModels']
        for rm_name in risk_models.keys():
            rm_parameters = risk_models[rm_name]
            rm_factory = RiskModelFactory()
            fsr = rm_factory.prepare(rm_name, stock_data_container_list=stock_data_container_list,
                                     parameter_dict=rm_parameters)
            fsr.determine_risk()

        self.assertEqual("FixedSizeRiskModel", stock_data_container_list[0].get_risk_model())

        # real calculation with real 52 w high value
        sb = round(calc_val * 1.005, 2)
        self.assertEqual(sb, stock_data_container_list[0].get_stop_buy())  # =23.5*1.005
        sl = round(sb * 0.97, 2)
        self.assertEqual(sl, stock_data_container_list[0].get_stop_loss())  # =23.5*1.005*0.97
        self.assertEqual(
            np.math.isclose(stock_data_container_list[0].get_position_size(), int(fixes_pos_size / sb), abs_tol=0.001),
            True)

    def test_RiskModelFactory__with_invalid_risk_model(self):
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
            ('2016-10-10', 23.62, 23.88, 23.55, 24.0, 44000),
            ('2016-10-11', 23.62, 30.0, 23.01, 23.16, 45000),
            ('2016-10-12', 23.16, 23.0, 23.11, 23.5, 46000)]

        df = DataFrame.from_records(data, columns=labels)
        stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [stock_data_container]

        rm_parameters = {}
        rm_factory = RiskModelFactory()
        self.assertRaises(NotImplementedError, rm_factory.prepare, "NotImplementedRiskModel",
                          stock_data_container_list=stock_data_container_list, parameter_dict=rm_parameters)
