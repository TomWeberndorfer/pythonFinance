from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Import the backtrader platform
import backtrader as bt
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
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        logger.info('%s, %s' % (dt.isoformat(), txt))

    def set_params(self, params):
        self.params = params

    def __init__(self, params):
        """
        Init method to wrap the ASTA-Strategy to the bt.Strategy
        :param params: Dict with parameters for testing, the Key "strategy_to_test" contains the strategy class to test.
        """

        if params['strategy_to_test'] is None or len(params['strategy_to_test']) <= 0:
            raise KeyError("params must contain key: strategy_to_test!")

        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.datavol = self.datas[0].volume
        self.datahi = self.datas[0].high
        self.datalo = self.datas[0].low
        self.buy_price = 0

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.highest_high = 0  # max (self.datahi)
        self.buyCnt = 0
        self.params = params
        self.stock_screener = StrategyFactory()

        # the params dict contains the strategy which is build with the string
        self.strategy_instance = self.stock_screener.prepare_strategy(self.params['strategy_to_test'],
                                                                      None,
                                                                      self.params['analysis_parameters'])

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
            date_time= self.datetime.date()
            data_name = hist_data._name

            long_stop = hist_data.close[0] - 5  # Will not be hit
            # Simply log the closing price of the series from the reference
            self.log('Data:' + str(data_name) + ', Close: ' + str(hist_data.close[0]) + ", volume: " + str(hist_data.volume[0]))

            # TODO den container anders --> ned so benennen
            df1 = convert_backtrader_to_dataframe(hist_data)
            # ticker not implemented, but not needed
            stock_data_container = StockDataContainer(data_name, "", "")
            stock_data_container.set_historical_stock_data(df1)
            stock_data_container_list.append(stock_data_container)

            results = self.strategy_instance.run_strategy(stock_data_container_list)

            pos = self.getposition(hist_data).size

            # Check if an order is pending ... if yes, we cannot send a 2nd one
            # TODO ??
            #if self.order:
            #    return

            # Check if we are in the market
            if not pos:
                if len(results) > 0:
                    self.buy_price = hist_data.close[0]

                    # num_of_pos_to_buy = round(self.params["fixed_pos_size"] / self.buy_price)
                    # self.buyCnt = num_of_pos_to_buy

                    buy_ord = self.order_target_percent(data=hist_data, target=self.params["position_size_percents"])
                    buy_ord.addinfo(name="Long Market Entry")
                    stop_size = buy_ord.size - abs(self.position.size)
                    self.sl_ord = self.sell(data=hist_data, size=stop_size, exectype=bt.Order.Stop, price=long_stop)
                    self.sl_ord.addinfo(name='Long Stop Loss')
