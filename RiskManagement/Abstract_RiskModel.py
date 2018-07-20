from abc import abstractmethod

from Utils.Abstract_SimpleMultithreading import Abstract_SimpleMultithreading


class Abstract_RiskModel(Abstract_SimpleMultithreading):

    def __init__(self, stock_data_container_list):
        self.stock_data_container_list = stock_data_container_list
        Abstract_SimpleMultithreading.__init__(self)

    def determine_risk(self, strategy_to_create, stock_data_container_list, parameter_list, all_news_text_list=None):
        strategy = self._create_strategy(strategy_to_create, stock_data_container_list, parameter_list,
                                         all_news_text_list)
        return strategy

    @abstractmethod
    def _method_to_execute(self, argument):
        """
        This method is abstract, implement the real list execution instead.
        :param argument: A single element of the list to execute
        :return: should return the result or add it to the list and return nothing
        """
        raise Exception("Abstractmethod")
