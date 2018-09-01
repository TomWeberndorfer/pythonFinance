# todo umstellen auf abstract factory
# https://sourcemaking.com/design_patterns/factory_method
from RiskManagement.Abstract_RiskModelFactory import Abstract_RiskModelFactory
from RiskManagement.ImplementedRiskModels.FixedSizeRiskModel import FixedSizeRiskModel
import os
from pathlib import Path
from Utils.CommonUtils import CommonUtils


class RiskModelFactory(Abstract_RiskModelFactory):

    @staticmethod
    def get_implemented_data_readers_dict():
        path = Path(os.path.dirname(os.path.abspath(__file__)))
        readers_dict = CommonUtils.get_implemented_items_dict(path, './*/**/**/*.py', "risk")
        return readers_dict

    def _create_risk_model(self, model_to_create, stock_data_container_list, parameter_dict):
        readers_dict = RiskModelFactory.get_implemented_data_readers_dict()

        if model_to_create in readers_dict:
            # get the class from class dict and create the concrete object then
            risk_model_class = readers_dict[model_to_create]
            risk_model = risk_model_class(stock_data_container_list, parameter_dict)
            return risk_model
        else:
            raise NotImplementedError("Risk Model is not implemented: " + str(model_to_create))
