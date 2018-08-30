from abc import abstractmethod


class Abstract_StrategyFactory:

    def prepare_strategy(self, strategy_to_create, stock_data_container_list, parameter_dict):
        strategy = self._create_strategy(strategy_to_create, stock_data_container_list, parameter_dict)
        return strategy

    @abstractmethod
    def _create_strategy(self, strategy_to_create, stock_data_container_list, parameter_list):
        raise Exception("Abstractmethod _create_strategy must be implemented!")

    @abstractmethod
    def get_implemented_strategies_dict(self):
        raise Exception("Abstractmethod get_implemented_strategies_dict must be implemented!")

    @staticmethod
    @abstractmethod
    def get_required_parameters_with_default_parameters(self):
        """
        Return a dict with required strategy parameters and default parameter values.
        :return: dict with required values and default parameters
        """
        raise Exception("Abstractmethod get_required_parameters_with_default_parameters must be implemented!")
