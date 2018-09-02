import traceback

from Utils.GlobalVariables import *
from Strategies.Abstract_StrategyFactory import Abstract_StrategyFactory
from pathlib import Path
from glob import glob
from Utils.CommonUtils import CommonUtils
from Utils.Logger_Instance import logger


class StrategyFactory(Abstract_StrategyFactory):

    @staticmethod
    def get_implemented_strategies_dict():
        path = Path(os.path.dirname(os.path.abspath(__file__)))
        strategy_dict = CommonUtils.get_implemented_items_dict(path, './*/**/**/*.py', "strat")
        return strategy_dict

    def _create_strategy(self, strategy_to_create, stock_data_container_list, parameter_dict):
        strategy_dict = StrategyFactory.get_implemented_strategies_dict()
        if strategy_to_create in strategy_dict:
            # get the class from class dict and create the concrete object than
            strat_class = strategy_dict[strategy_to_create]
            strategy = strat_class(stock_data_container_list, parameter_dict)
            return strategy
        else:
            raise NotImplementedError("Strategy is not implemented: " + str(strategy_to_create))

    @staticmethod
    def get_required_parameters_with_default_parameters():
        """
        Return a dict with required strategy parameters and default parameter values.
        :return: dict with required values and default parameters
        """
        all_strategy_parameters_dict = {}
        strategies_dict = StrategyFactory.get_implemented_strategies_dict()

        for strat_class_key in list(strategies_dict.keys()):
            try:
                def_params = strategies_dict[strat_class_key].get_required_parameters_with_default_parameters()
                all_strategy_parameters_dict.update(def_params)
            except NotImplementedError as nie:
                logger.error("Exception for strategy class " + strat_class_key + ": " + str(nie) + "\n" + str(
                    traceback.format_exc()))

        all_strategy_parameters_dict = {'Strategies': all_strategy_parameters_dict}
        other_params = StrategyFactory.get_other_parameters_with_default_parameters()
        all_strategy_parameters_dict.update(other_params)

        backtesting_params = StrategyFactory.get_backtesting_parameters_with_default_parameters()
        all_strategy_parameters_dict.update(backtesting_params)

        return all_strategy_parameters_dict

    @staticmethod
    def get_other_parameters_with_default_parameters():
        """
        Return a dict with required other parameters and default parameter values.
        :return: dict with required values and default parameters
        """
        stock_data_file = GlobalVariables.get_data_files_path() + "stock_data_container_file.pickle"
        other_params = {'stock_data_container_file': stock_data_file, 'list_with_stock_pages_to_read': {
            'SP500': {'websource_address': "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                      'find_name': 'table', 'class_name': 'class', 'table_class': 'wikitable sortable',
                      'ticker_column_to_read': 0, 'name_column_to_read': 1, 'stock_exchange': 'en'}},
                        'RiskModels': {
                            'FixedSizeRiskModel': {'OrderTarget': 'order_target_value', 'TargetValue': 2500}}}

        other_parameters_dict = {"OtherParameters": other_params}

        return other_parameters_dict

    @staticmethod
    def get_backtesting_parameters_with_default_parameters():
        """
        Return a dict with required backtesting parameters and default parameter values.
        :return: dict with required values and default parameters
        :key trade_commission_percent: Trading commission for every buy/sell in percent of order in percent
        :key initial_cash: Initial cash to trade with.
        """
        backtesting_parameters = {'initial_cash': 30000, 'trade_commission_percent': 0.005}
        parameters_dict = {"BacktestingParameters": backtesting_parameters}

        return parameters_dict
