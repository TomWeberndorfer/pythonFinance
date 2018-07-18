from abc import abstractmethod


class Abstract_StockFactory():
    def prepare_strategy(self, strategy_to_create, stock_data_container_list, parameter_list, all_news_text_list=None):
        strategy = self._create_strategy(strategy_to_create, stock_data_container_list, parameter_list,
                                         all_news_text_list)
        return strategy

    @abstractmethod
    def _create_strategy(self, strategy_to_create, stock_data_container_list, parameter_list, all_news_text_list):
        raise Exception("Abstractmethod")
