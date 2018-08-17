from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Import the backtrader platform
import backtrader as bt

from DataReading.StockDataContainer import StockDataContainer
from Strategies.StrategyFactory import StrategyFactory
from Utils.common_utils import convert_backtrader_to_dataframe

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
        print('%s, %s' % (dt.isoformat(), txt))

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
            print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
            print('{} Order Accepted'.format(order.info['name']))
            print('{}, Status {}: Ref: {}, Size: {}, Price: {}, Position: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                'NA' if not order.price else round(order.price, 5),
                'NA' if not order.price else round(order.price * order.size, 5)
            ))
            buy_data.append((date, order.price))

        if order.status == order.Completed:
            print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
            print('{} Order Completed'.format(order.info['name']))
            print('{}, Status {}: Ref: {}, Size: {}, Price: {}, Position: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                'NA' if not order.price else round(order.price, 5),
                'NA' if not order.price else round(order.price * order.size, 5)
            ))
            print('Created: {} Price: {} Size: {}'.format(bt.num2date(order.created.dt), order.created.price,
                                                          order.created.size))
            print('-' * 80)

        if order.status == order.Canceled:
            print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
            print('{} Order Canceled'.format(order.info['name']))
            print('{}, Status {}: Ref: {}, Size: {}, Price: {}, Position: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                'NA' if not order.price else round(order.price, 5),
                'NA' if not order.price else round(order.price * order.size, 5)
            ))

        if order.status == order.Rejected:
            print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
            print('WARNING! {} Order Rejected'.format(order.info['name']))
            print('{}, Status {}: Ref: {}, Size: {}, Price: {}, Position: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                'NA' if not order.price else round(order.price, 5),
                'NA' if not order.price else round(order.price * order.size, 5)
            ))
            print('-' * 80)

    def notify_trade(self, trade):
        date = self.data.datetime.datetime()
        if trade.isclosed:
            print('-' * 32, ' NOTIFY TRADE ', '-' * 32)
            print('{}, Close Price: {}, Profit, Gross {}, Net {}'.format(
                date,
                trade.price,
                round(trade.pnl, 2),
                round(trade.pnlcomm, 2)))
            print('-' * 80)
            buy_data.append((date, trade.price))

    ###########

    def next(self):
        """
        Method which is executed while running backtest.
        Must implement the real strategy.
        :return:
        """
        long_stop = self.data.close[0] - 5  # Will not be hit
        # Simply log the closing price of the series from the reference
        self.log('Close: ' + str(self.dataclose[0]) + ", volume: " + str(self.datavol[0]))

        # TODO den container anders --> ned so benennen
        df1 = convert_backtrader_to_dataframe(self.datas[0])
        stock_name = self.datas[0]._name
        # TODO ticker not implemented
        stock_data_container = StockDataContainer(stock_name, "TEMPXY", "")
        stock_data_container.set_historical_stock_data(df1)
        stock_data_container_list = [stock_data_container]

        results = self.strategy_instance.run_strategy(stock_data_container_list)

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            if len(results) > 0:
                self.buy_price = self.dataclose[0]

                # num_of_pos_to_buy = round(self.params["fixed_pos_size"] / self.buy_price)
                # self.buyCnt = num_of_pos_to_buy

                buy_ord = self.order_target_percent(target=self.params["position_size_percents"])
                buy_ord.addinfo(name="Long Market Entry")
                stop_size = buy_ord.size - abs(self.position.size)
                self.sl_ord = self.sell(size=stop_size, exectype=bt.Order.Stop, price=long_stop)
                self.sl_ord.addinfo(name='Long Stop Loss')
