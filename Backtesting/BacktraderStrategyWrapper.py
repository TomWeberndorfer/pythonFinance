from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Import the backtrader platform
import backtrader as bt
import os
import pandas as pd
from DataContainerAndDecorator.NewsDataContainerDecorator import NewsDataContainerDecorator
from Utils.Logger_Instance import logger
from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Strategies.StrategyFactory import StrategyFactory
from Utils.StockDataUtils import convert_backtrader_to_dataframe

####################################
# https://www.backtrader.com/docu/indautoref.html
#
####################################
# Create a Stratey
buy_data = []


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
        self.strategy_instance = self.stock_screener.prepare_strategy(self.strategy_to_test, **kwargs)

        # only one risk model can be used, the first risk model to be taken
        risk_model = self.risk_model
        order_target = risk_model['OrderTarget']
        self.order_target_method = self._get_order_target(order_target)

        self.order_parameter_value = risk_model['TargetValue']

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
            logger.info('--------- NOTIFY ORDER ---------')
            logger.info('{} Order Accepted'.format(order.info['name']))
            logger.info('{}, Status {}: Ref: {}, Size: {}, Price: {}, Position: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                'NA' if not order.price else round(order.price, 5),
                'NA' if not order.price else round(order.price * order.size, 5)
            ))
            buy_data.append((date, order.price))

        if order.status == order.Completed:
            logger.info('--------- NOTIFY ORDER ---------')
            logger.info('{} Order Completed'.format(order.info['name']))
            logger.info('{}, Status {}: Ref: {}, Size: {}, Price: {}, Position: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                'NA' if not order.price else round(order.price, 5),
                'NA' if not order.price else round(order.price * order.size, 5)
            ))
            logger.info('Created: {} Price: {} Size: {}'.format(bt.num2date(order.created.dt), order.created.price,
                                                                order.created.size))
            logger.info('----------')

        if order.status == order.Canceled:
            logger.info('--------- NOTIFY ORDER ---------')
            logger.info('{} Order Canceled'.format(order.info['name']))
            logger.info('{}, Status {}: Ref: {}, Size: {}, Price: {}, Position: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                'NA' if not order.price else round(order.price, 5),
                'NA' if not order.price else round(order.price * order.size, 5)
            ))

        if order.status == order.Rejected:
            logger.info('--------- NOTIFY ORDER ---------')
            logger.info('WARNING! {} Order Rejected'.format(order.info['name']))
            logger.info('{}, Status {}: Ref: {}, Size: {}, Price: {}, Position: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                'NA' if not order.price else round(order.price, 5),
                'NA' if not order.price else round(order.price * order.size, 5)
            ))
            logger.info('----------')

    def notify_trade(self, trade):
        date = self.data.datetime.datetime()
        if trade.isclosed:
            logger.info('---------  NOTIFY TRADE  ---------')
            logger.info('{}, Close Price: {}, Profit, Gross {}, Net {}'.format(
                date,
                trade.price,
                trade.data._name,
                round(trade.pnl, 2),
                round(trade.pnlcomm, 2)))
            logger.info('----------')
            buy_data.append((date, trade.price))

    ###########

    def next(self):
        """
        Method which is executed while running backtest.
        Must implement the real strategy.
        :return:
        """
        # TODO https://backtest-rookies.com/2017/08/22/backtrader-multiple-data-feeds-indicators/
        stock_data_container_list = []

        for i, hist_data in enumerate(self.datas):
            date_time = self.datetime.date()
            stock_name = hist_data._name
            dataname = hist_data._dataname

            curr_news = ""
            # add the news text because backtrader does not support news
            # data from pandas do not have a name --> not add news
            if isinstance(dataname, str):
                news_data = self.news_data_dict[dataname]
                if hasattr(news_data, "NewsText") and hasattr(news_data, "Date"):
                    for currEntry in range(0, len(news_data.Date)):
                        if str(date_time) in news_data.Date[currEntry]:
                            try:
                                curr_news = str(news_data.NewsText[currEntry])
                            except Exception as e:
                                pass
                            break

            long_stop = hist_data.close[0] - 5  # Will not be hit
            # Simply log the closing price of the series from the reference
            self.log('Time:' + str(date_time) + ', Data:' + str(stock_name) + ', Close: ' + str(
                hist_data.close[0]) + ", volume: " + str(hist_data.volume[0]))

            # TODO den container anders --> ned so benennen
            df1 = convert_backtrader_to_dataframe(hist_data)
            # ticker not implemented, but not needed
            stock_data_container = StockDataContainer(stock_name, "", "")
            stock_data_container.set_historical_stock_data(df1)
            news_dec = NewsDataContainerDecorator(stock_data_container, 0, 0, curr_news, 0)
            stock_data_container_list.append(news_dec)
            results = self.strategy_instance.run_strategy(stock_data_container_list)

            pos = self.getposition(hist_data).size
            # Check if we are in the market
            if not pos:
                if len(results) > 0:
                    self.buy_price = hist_data.close[0]
                    buy_ord = self.order_target_method(data=hist_data, target=self.order_parameter_value)
                    buy_ord.addinfo(name="Long Market Entry")
                    stop_size = buy_ord.size - abs(self.position.size)
                    self.sl_ord = self.sell(data=hist_data, size=stop_size, exectype=bt.Order.Stop, price=long_stop)
                    self.sl_ord.addinfo(name='Long Stop Loss')

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
