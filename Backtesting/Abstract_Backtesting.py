class Abstract_Backtesting:

    def run_test(self, data_list, strategy_to_test, backtesting_parameters, analysis_parameters, risk_model,
                 news_data, analyzers=[], **kwargs):
        """
        Run method for the wrapper which wrap the ASTA-Framework structure to backtesting framework structure.
        :param news_data: news data in string form
        :param analysis_parameters: dict with analysis parameters for strategy
        :param strategy_to_test: name of the strategy as string
        :param data_list: a list with historical stock data in bt-format
        :param backtesting_parameters: Dict with parameters for testing, the Key "strategy_to_test" contains the strategy class to test.
        :param analyzers: List with class of btanalyzer, ex.: [btanalyzer.TradeAnalyzer]
        :param risk_model: other testing relevant parameters as dict
        :param kwargs: https://stackoverflow.com/questions/1769403/understanding-kwargs-in-python
        :return: backtesting_result_instance final instance with plot property
        :return: test result with analyzers properties to get
        """
        raise NotImplementedError("run_test is not implemented!")
