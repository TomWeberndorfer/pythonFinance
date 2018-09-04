from abc import abstractmethod


class Abstract_BacktestingFactory:
    def prepare(self, backtest_to_create, stock_data_container_list,
                reload_stockdata, parameter_dict):
        storage = self._create_backtester(backtest_to_create, stock_data_container_list,
                                          reload_stockdata, parameter_dict)
        return storage

    @abstractmethod
    def _create_backtester(self, reader_to_create, stock_data_container_list,
                           reload_stockdata, parameter_dict):
        raise Exception("Abstractmethod")
