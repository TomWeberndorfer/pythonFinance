import traceback
from pathlib import Path

from Utils.Abstract_Factory import Abstract_Factory
from Utils.GlobalVariables import *
from Utils.Logger_Instance import logger


class StrategyFactory(Abstract_Factory):

    def __init__(self):
        path = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(path, './*/**/**/*.py', 'strat')

    @staticmethod
    def get_required_parameters_with_default_parameters():
        """
        Return a dict with required strategy parameters and default parameter values.
        :return: dict with required values and default parameters
        """
        all_strategy_parameters_dict = {}
        strat_factory = StrategyFactory()
        strategies_dict = strat_factory.get_implemented_classes()

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

        # TODO insert:
        # ['http://topforeignstocks.com/stock-lists/the-list-of-listed-companies-in-germany/',
        # 'tbody', 'class', 'row-hover', 2, 1, 'de']]

        stock_data_file = GlobalVariables.get_data_files_path() + "stock_data_container_file.pickle"
        other_params = {'stock_data_container_file': stock_data_file,
                        'dict_with_stock_pages_to_read': {
                            'SP500': {'websource_address': "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                                      'find_name': 'table', 'class_name': 'class', 'table_class': 'wikitable sortable',
                                      'ticker_column_to_read': 0, 'name_column_to_read': 1, 'stock_exchange': 'en'},
                            'DAX': {
                                'websource_address': "http://topforeignstocks.com/stock-lists/the-list-of-listed-companies-in-germany/",
                                'find_name': 'tbody', 'class_name': 'class', 'table_class': 'row-hover',
                                'ticker_column_to_read': 2, 'name_column_to_read': 1, 'stock_exchange': 'de'}},
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
        backtesting_parameters = {'BacktestingFramework': 'BacktraderWrapper',
                                  'BacktestingFramework': 'BacktraderWrapper', 'initial_cash': 30000,
                                  'trade_commission_percent': 0.005}
        parameters_dict = {"BacktestingParameters": backtesting_parameters}

        return parameters_dict
