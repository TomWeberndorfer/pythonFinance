from abc import abstractmethod
from Utils.GlobalVariables import *
from RiskManagement.Abstract_RiskModel import Abstract_RiskModel
from Utils.Abstract_SimpleMultithreading import Abstract_SimpleMultithreading
from Utils.Logger_Instance import logger
from Utils.common_utils import calculate_stopbuy_and_stoploss


class FixedSizeRiskModel(Abstract_RiskModel):

    def _method_to_execute(self, stock_data_container):
        """
        This method is abstract, implement the real list execution instead.
        :param stock_data_container: A single element of the list to execute
        :return: should return the result or add it to the list and return nothing
        """

        res = calculate_stopbuy_and_stoploss(stock_data_container.historical_stock_data())
        sl = res['stop_loss']
        sb = res['stop_buy']
        # cut the comma value to avoid position size above the fixes size maximum
        if sb is not 'NaN':
            num_of_pos_to_buy = int(self._parameter_dict["FixedPositionSize"] / sb)
            stock_data_container.set_position_size(num_of_pos_to_buy)
            stock_data_container.set_stop_buy(round(sb, 2))
        else:
            stock_data_container.set_position_size('NaN')
            stock_data_container.set_stop_buy('NaN')

        if sl is not 'NaN':
            stock_data_container.set_stop_loss(round(sl, 2))
        else:
            stock_data_container.set_stop_loss('NaN')

        stock_data_container.set_risk_model("FixedSizeRiskModel")
