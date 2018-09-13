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
        other_params = GlobalVariables.get_other_parameters_with_default_parameters()
        all_strategy_parameters_dict.update({"OtherParameters": other_params})

        backtesting_params = GlobalVariables.get_backtesting_parameters_with_default_parameters()
        all_strategy_parameters_dict.update(backtesting_params)

        return all_strategy_parameters_dict
