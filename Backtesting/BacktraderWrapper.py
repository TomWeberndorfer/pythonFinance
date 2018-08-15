import backtrader as bt
from Backtesting.BacktraderStrategyWrapper import BacktraderStrategyWrapper


class BacktraderWrapper:
    def run_test(self, data_list, initial_cash=10000, trade_commission_percent=0.005,
                 analyzers=[], plot_result=True, params={}):
        """
        Run method for the wrapper which wrap the ASTA-Framework structure to backtrader structure.
        :param data_list: a list with historical stock data in bt-format
        :param params: Dict with parameters for testing, the Key "strategy_to_test" contains the strategy class to test.
        :param plot_result: Plot results in candle stick chart (disable it for unit testing)
        :param analyzers: List with class of btanalyzer, ex.: [btanalyzer.TradeAnalyzer]
        :param trade_commission_percent: Trading commission for every buy/sell in percent of order
        :param initial_cash: Initial cash to trade with.
        :param percentage_transaction_costs: Percentage of the position size which costs to buy/sell
        :param bt_analyzers: a list with analyzer classes to add
        """
        cerebro = bt.Cerebro()

        # add the backtrader strategy wrapper, the real strategy will be build there with the params dict
        cerebro.addstrategy(BacktraderStrategyWrapper, params)

        if isinstance(data_list, list):
            for data in data_list:
                cerebro.adddata(data)
        else:
            raise NotImplementedError("Data must be a list")

        # Set our desired cash start
        cerebro.broker.setcash(initial_cash)

        for analyzer in analyzers:
            cerebro.addanalyzer(analyzer)

        # Set the commission
        # https://www.backtrader.com/docu/commission-schemes/commission-schemes.html
        # 0.5% of the operation value --> 2500 € --> 12.5 per Buy/Sell
        cerebro.broker.setcommission(commission=trade_commission_percent)
        # Print out the starting conditions
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

        backtest_result = cerebro.run()
        analyzers = backtest_result[0].analyzers

        for analyzer in analyzers:
            test = analyzer.get_analysis()
            print(str(analyzer) + ": " + str(test))

        # Print out the final result
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

        # Plot the result
        if plot_result:
            cerebro.plot(style='candlestick', barup='green', bardown='red')
