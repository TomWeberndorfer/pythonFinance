from Strategies.GapUpHighVolumeStrategy import GapUpHighVolumeStrategy
from Strategies.SimplePatternNewsStrategy import SimplePatternNewsStrategy
from Strategies.W52HighTechnicalStrategy import W52HighTechnicalStrategy
from Utils.GlobalVariables import *
from Strategies.Abstract_StrategyFactory import Abstract_StrategyFactory


class StrategyFactory(Abstract_StrategyFactory):

    @staticmethod
    def get_implemented_strategies_list():
        # TODO imports must be there, else not able to get globals()
        return ["SimplePatternNewsStrategy", "W52HighTechnicalStrategy"]  # TODO, "GapUpHighVolumeStrategy"]

    def _create_strategy(self, strategy_to_create, stock_data_container_list, parameter_dict):
        strategy = None
        strategies_list = StrategyFactory.get_implemented_strategies_list()

        # check if this strategy is implemented
        if strategy_to_create in strategies_list:
            # create a class variable from string
            strat_class = globals()[strategy_to_create]
            strategy = strat_class(stock_data_container_list, parameter_dict)
        else:
            raise NotImplementedError("Strategy is not implemented: " + str(strategy_to_create))

        return strategy

    @staticmethod
    def get_required_parameters_with_default_parameters():
        """
        Return a dict with required strategy parameters and default parameter values.
        :return: dict with required values and default parameters
        """
        all_strategy_parameters_dict = {}
        strategies_list = StrategyFactory.get_implemented_strategies_list()

        for strat in strategies_list:
            strat_class = globals()[strat]
            def_params = strat_class.get_required_parameters_with_default_parameters()
            all_strategy_parameters_dict.update(def_params)

        stock_data_file = GlobalVariables.get_data_files_path() + "stock_data_container_file.pickle"
        other_params = {'stock_data_container_file': stock_data_file, 'list_with_stock_pages_to_read': {
            'SP500': {'websource_address': "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                      'find_name': 'table', 'class_name': 'class', 'table_class': 'wikitable sortable',
                      'ticker_column_to_read': 0, 'name_column_to_read': 1, 'stock_exchange': 'en'}},
                        'RiskModels': {'FixedSizeRiskModel': {'FixedPositionSize': 2500}}}

        all_strategy_parameters_dict = {'Strategies': all_strategy_parameters_dict}
        all_strategy_parameters_dict.update({"OtherParameters": other_params})

        return all_strategy_parameters_dict
