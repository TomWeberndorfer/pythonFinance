import backtrader as bt
from Backtesting.BacktraderStrategyWrapper import BacktraderStrategyWrapper
import logging
from Utils.Logger_Instance import logger


class BacktraderWrapper:
    def run_test(self, data_list, strategy_to_test, backtesting_parameters, analysis_parameters, risk_model,
                 news_data={}, analyzers=[], **kwargs):
        """
        Run method for the wrapper which wrap the ASTA-Framework structure to backtrader structure.
        :param news_data:
        :param analysis_parameters: dict with analysis parameters for strategy
        :param strategy_to_test: name of the strategy as string
        :param data_list: a list with historical stock data in bt-format
        :param backtesting_parameters: Dict with parameters for testing, the Key "strategy_to_test" contains the strategy class to test.
        :param analyzers: List with class of btanalyzer, ex.: [btanalyzer.TradeAnalyzer]
        :param risk_model: other testing relevant parameters as dict
        :return: cerebro final instance, backtrader test result
        """
        cerebro = bt.Cerebro()

        # add the backtrader strategy wrapper, real strategy will be build there with the backtesting_parameters dict
        # cerebro.addstrategy(BacktraderStrategyWrapper, all_parameter, news_data)
        cerebro.addstrategy(BacktraderStrategyWrapper, strategy_to_test=strategy_to_test,
                            backtesting_parameters=backtesting_parameters,
                            news_data=news_data, analysis_parameters=analysis_parameters, risk_model=risk_model,
                            **kwargs)

        if isinstance(data_list, list):
            for data in data_list:
                cerebro.adddata(data, name=data._name)

        else:
            raise NotImplementedError("Data must be a list")

        # Set our desired cash start
        cerebro.broker.setcash(backtesting_parameters['initial_cash'])

        for analyzer in analyzers:
            cerebro.addanalyzer(analyzer)

        # Set the commission
        # https://www.backtrader.com/docu/commission-schemes/commission-schemes.html
        # 0.5% of the operation value --> 2500 € --> 12.5 per Buy/Sell
        cerebro.broker.setcommission(commission=backtesting_parameters['trade_commission_percent'])
        # Print out the starting conditions
        logger.info('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

        backtest_result = cerebro.run()
        analyzers = backtest_result[0].analyzers

        for analyzer in analyzers:
            test = analyzer.get_analysis()
            logger.info(str(analyzer) + ": " + str(test))

        # Print out the final result
        logger.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

        return cerebro, backtest_result
