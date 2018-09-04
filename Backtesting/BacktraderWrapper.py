from os.path import basename

import backtrader as bt

from Backtesting.Abstract_Backtesting import Abstract_Backtesting
from Backtesting.BacktraderStrategyWrapper import BacktraderStrategyWrapper
import logging
from Utils.Logger_Instance import logger
import backtrader.feeds as btfeeds
from Utils.GlobalVariables import GlobalVariables


class BacktraderWrapper(Abstract_Backtesting):
    def run_test(self, data_file_list, strategy_to_test, backtesting_parameters, analysis_parameters, risk_model,
                 analyzers=[], **kwargs):
        """
        Run method for the wrapper which wrap the ASTA-Framework structure to backtrader structure.
        :param analysis_parameters: dict with analysis parameters for strategy
        :param strategy_to_test: name of the strategy as string
        :param data_file_list: a list with files to read as string
        :param backtesting_parameters: Dict with parameters for testing, the Key "strategy_to_test" contains the strategy class to test.
        :param analyzers: List with class of btanalyzer, ex.: [btanalyzer.TradeAnalyzer]
        :param risk_model: other testing relevant parameters as dict
        :return: backtesting_result_instance final instance, backtrader test result
        """
        cerebro = bt.Cerebro()

        # add the backtrader strategy wrapper, real strategy will be build there with the backtesting_parameters dict
        # backtesting_result_instance.addstrategy(BacktraderStrategyWrapper, all_parameter, news_data)
        cerebro.addstrategy(BacktraderStrategyWrapper, strategy_to_test=strategy_to_test,
                            backtesting_parameters=backtesting_parameters,
                            analysis_parameters=analysis_parameters, risk_model=risk_model,
                            **kwargs)

        # load the data from given file list and add it to backtrader instance
        if isinstance(data_file_list, list):
            for file_path in data_file_list:
                if isinstance(file_path, str):
                    stock_name = basename(file_path)
                    data = btfeeds.GenericCSVData(
                        name=stock_name,
                        dataname=file_path,
                        dtformat=GlobalVariables.get_stock_data_dtformat(),
                        nullvalue=0.0,
                        datetime=0,
                        open=1, high=2, low=3,
                        close=4, volume=5,
                        openinterest=-1)
                    cerebro.adddata(data, name=data._name)
                else:
                    # compatibility for backtrader pandas data feed
                    cerebro.adddata(file_path, name=file_path._name)

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
