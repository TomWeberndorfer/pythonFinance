from RiskManagement.Abstract_RiskModel import Abstract_RiskModel
from Utils.StockDataUtils import calculate_stopbuy_and_stoploss


class FixedSizeRiskModel(Abstract_RiskModel):

    def _method_to_execute(self, stock_data_container):
        """
        This method is abstract, implement the real list execution instead.
        :param stock_data_container: A single element of the list to execute
        :return: should return the result or add it to the list and return nothing
        """

        sl, sb = calculate_stopbuy_and_stoploss(stock_data_container.historical_stock_data())
        # cut the comma value to avoid position size above the fixes size maximum
        if sb is not 0:
            num_of_pos_to_buy = int(self.parameter_dict["TargetValue"] / sb)
            stock_data_container.set_position_size(num_of_pos_to_buy)
            stock_data_container.set_stop_buy(round(sb, 2))
        else:
            stock_data_container.set_position_size(0)
            stock_data_container.set_stop_buy(0)

        if sl is not 0:
            stock_data_container.set_stop_loss(round(sl, 2))
        else:
            stock_data_container.set_stop_loss(0)

        stock_data_container.set_risk_model("FixedSizeRiskModel")
        assert stock_data_container.get_risk_model() in "FixedSizeRiskModel"
