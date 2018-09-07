from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Import the backtrader platform
import backtrader as bt
import os
import pandas as pd
from DataContainerAndDecorator.NewsDataContainerDecorator import NewsDataContainerDecorator
from RiskManagement.RiskModelFactory import RiskModelFactory
from Utils.Logger_Instance import logger
from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Strategies.StrategyFactory import StrategyFactory
from Utils.StockDataUtils import convert_backtrader_to_dataframe, convert_backtrader_to_asta_data

####################################
# https://www.backtrader.com/docu/indautoref.html
#
####################################
# Create a Straty


class BacktraderStrategyWrapper(bt.Strategy):

    def log(self, txt, dt=None):
        """ Logging function fot this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        logger.info('%s, %s' % (dt.isoformat(), txt))

    def __init__(self, **kwargs):
        """
        Init method to wrap the ASTA-Strategy to the bt.Strategy
        :param kwargs: Dict with parameters for testing, the Key "strategy_to_test" contains the strategy class to test.
        """

        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.datavol = self.datas[0].volume
        self.datahi = self.datas[0].high
        self.datalo = self.datas[0].low
        self.buy_price = 0

        # set the given values in self
        for key, value in kwargs.items():
            setattr(self, key, value)

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.highest_high = 0  # max (self.datahi)
        self.buyCnt = 0

        self.stock_screener = StrategyFactory()

        # the parameter dict contains the strategy which is build with the string
        self.strategy_instance = self.stock_screener.prepare(self.strategy_to_test, **kwargs)

        # only one risk model can be used, the first risk model to be taken
        first_rm_key = list(self.risk_model.keys())[0]
        self.curr_risk_model = self.risk_model[first_rm_key]
        self.order_target_method = self._get_order_target(self.curr_risk_model['OrderTarget'])
        self.news_data_dict = {}

        # add the news text because backtrader does not support news
        # data from pandas do not have a name --> not add news
        for i, hist_data in enumerate(self.datas):
            dataname = hist_data._dataname
            if isinstance(dataname, str) and os.path.exists(dataname):
                news_data = pd.read_csv(dataname)
                self.news_data_dict.update({dataname: news_data})

    ###############
    def notify_order(self, order):
        date = self.data.datetime.datetime().date()

        if order.status == order.Accepted:
            self._log_order(date, order, "Accepted")

        if order.status == order.Completed:
            self._log_order(date, order, "Completed")

        if order.status == order.Canceled:
            self._log_order(date, order, "Canceled")

        if order.status == order.Rejected:
            self._log_order(date, order, "Rejected")

    def notify_trade(self, trade):
        date = self.data.datetime.datetime()
        if trade.isclosed:
            logger.info('---------  NOTIFY TRADE  ---------')
            logger.info('   {}, Close Price: {}, Profit, Gross {}, Net {}'.format(
                date,
                trade.price,
                trade.data._name,
                round(trade.pnl, 2),
                round(trade.pnlcomm, 2)))
            logger.info('----------')

    ###########

    def next(self):
        """
        Method which is executed while running backtest.
        Must implement the real strategy.
        :return:
        """
        # TODO https://backtest-rookies.com/2017/08/22/backtrader-multiple-data-feeds-indicators/

        for i, hist_data in enumerate(self.datas):
            stock_data_container_list = []
            date_time = self.datetime.date()
            stock_name = hist_data._name

            self.log('Close: ' + str(
                hist_data.close[0]) + ", volume: " + str(hist_data.volume[0]) + ', Datasource: ' + str(stock_name))

            # TODO print anything to indicate a news in gui
            # TODO https://www.backtrader.com/docu/extending-a-datafeed.html
            # TODO ex: btind.SMA(self.data.pe, period=1, subplot=False) for data of classification

            convert_backtrader_to_asta_data(hist_data, self.news_data_dict, date_time, stock_data_container_list)
            # test only one strategy, first one --> [0]
            self.strategy_instance.run_strategy(stock_data_container_list)

            pos = self.getposition(hist_data).size
            # Check if we are in the market
            if not pos:
                # TODO insert sell for short strategies too
                # check if buy
                try:
                    if len(stock_data_container_list) > 0 and 'buy' in \
                            stock_data_container_list[0].get_recommendation_strategies()[self.strategy_to_test][
                                0].lower():
                        # test only first risk model --> [0]
                        rm_factory = RiskModelFactory()
                        first_rm_key = list(self.risk_model.keys())[0]
                        risk_model = self.risk_model[first_rm_key]
                        fsr = rm_factory.prepare(first_rm_key, stock_data_container_list=stock_data_container_list,
                                                 parameter_dict=risk_model)
                        fsr.determine_risk()

                        # TODO checken ob da ned zwei stop order draus gemacht werden
                        # --> TODO order long - stop bearbeiten
                        # einstiegskurs nicht nach strategie sondern gleich

                        # buy the stock
                        self.buy_price = hist_data.close[0]
                        buy_ord = self.order_target_method(data=hist_data, target=self.curr_risk_model['TargetValue'])
                        buy_ord.addinfo(name="Long Market Entry")

                        # get the stop loss value for risk avoiding
                        long_stop = stock_data_container_list[0].get_stop_loss()
                        stop_size = buy_ord.size - abs(self.position.size)
                        self.sl_ord = self.sell(data=hist_data, size=stop_size, exectype=bt.Order.Stop, price=long_stop)
                        self.sl_ord.addinfo(name='Long Stop Loss')
                except Exception as e:
                    print(e)

    def _get_order_target(self, order_type_str):
        """
        Get the method of the backtrader order target.
        size -> amount of shares, contracts in the portfolio of a specific asset
        value -> value in monetary units of the asset in the portfolio
        percent -> percentage (from current portfolio) value of the asset in the current portfolio
        :param order_type_str: type or part of the type as string
        :return: target bounded method
        """
        order_target = None

        if order_type_str in "order_target_size":
            order_target = self.order_target_size
        elif order_type_str in "order_target_value":
            order_target = self.order_target_value
        elif order_type_str in "order_target_percent":
            order_target = self.order_target_percent
        else:
            raise NotImplementedError("Order target " + str(order_type_str) + " is not implemented!")

        return order_target

    def _log_order(self, date, order, text):
        logger.info('---------  NOTIFY ORDER:')
        logger.info(('  {} Order ' + text).format(order.info['name']))
        logger.info('   {}, Status {}: Ref: {}, Size: {}, Price: {}, Position: {}'.format(
            date,
            order.status,
            order.ref,
            order.size,
            'NA' if not order.price else round(order.price, 5),
            'NA' if not order.price else round(order.price * order.size, 5)
        ))
