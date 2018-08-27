from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Import the backtrader platform
import backtrader as bt

####################################
# https://www.backtrader.com/docu/indautoref.html
#
####################################


# Create a Stratey
from pandas import DataFrame

from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Strategies.StrategyFactory import StrategyFactory
from Utils.GlobalVariables import *
from Utils.common_utils import convert_backtrader_to_dataframe

buy_data = []
P = 10000
c = 0.99  # 99% confidence interval
com = 0.005


class TestStrategy_1(bt.Strategy):
    params = (('position_size_percents', 0.2),)

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.datavol = self.datas[0].volume
        self.datahi = self.datas[0].high
        self.datalo = self.datas[0].low
        # self.dataclose = self.datas[0][GlobalVariables.get_stock_data_labels_dict()['Close']]
        # self.datavol = self.datas[0][GlobalVariables.get_stock_data_labels_dict()['Volume']]
        # self.datahi = self.datas[0][GlobalVariables.get_stock_data_labels_dict()['High']]
        # self.datalo = self.datas[0][GlobalVariables.get_stock_data_labels_dict()['Low']]
        self.buy_price = 0

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        # self.sma = bt.indicators.SimpleMovingAverage(
        # self.datas[0], period=self.params.maperiod)

        self.highest_high = 0  # max (self.datahi)
        self.buyCnt = 0

        # Indicators for the plotting show

        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
        #                                     subplot=True)
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.ATR(self.datas[0], plot=False)

        ##################################################
        # 52 w strategy
        self.w52hi_parameter_dict = {'check_days': 5, 'min_cnt': 3, 'min_vol_dev_fact': 1.2,
                                     'within52w_high_fact': 0.99}
        self.stock_screener = StrategyFactory()

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
        long_stop = self.data.close[0] - 5  # Will not be hit
        # Simply log the closing price of the series from the reference
        self.log('Close: ' + str(self.dataclose[0]) + ", volume: " + str(self.datavol[0]))
        # self.log(' from 1: Close: ' + str(self.dataclose[1]) + ", volume: " + str(self.datavol[1]))

        df1 = convert_backtrader_to_dataframe(self.datas[0])
        stock_data_container = StockDataContainer("Autodesk Inc.", "ADSK", "")
        stock_data_container.set_historical_stock_data(df1)
        stock_data_container_list = [stock_data_container]

        w52_hi_strat = self.stock_screener.prepare_strategy("W52HighTechnicalStrategy",
                                                            stock_data_container_list,
                                                            self.w52hi_parameter_dict)

        results = w52_hi_strat.run_strategy()

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            if len(results) > 0:
                # if raise_cnt < 3:
                self.buy_price = self.dataclose[0]
                # self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                # self.order = self.buy()
                # self.buyCnt = round((cerebro.broker.cash / self.dataclose[0]/10))  # TODO
                initcash = 10000
                fixed_pos_size = 2500
                num_of_max_position = 10

                num_of_pos_to_buy = round(fixed_pos_size / self.buy_price)
                self.buyCnt = num_of_pos_to_buy
                # self.buy(size=self.buyCnt)
                # For a StopTrail going downwards with 2% distance
                # self.buy(size=1, exectype=bt.Order.StopTrail, trailpercent=0.02)  # last price will be used as reference
                buy_ord = self.order_target_percent(target=self.p.position_size_percents)
                buy_ord.addinfo(name="Long Market Entry")
                stop_size = buy_ord.size - abs(self.position.size)
                self.sl_ord = self.sell(size=stop_size, exectype=bt.Order.Stop, price=long_stop)
                self.sl_ord.addinfo(name='Long Stop Loss')

        # TODO add a sell strategy, others to stop loss
        # else:
        # cur_val = self.datalo[0]
        # if cur_val > self.buy_price:
        #     self.buy_price = cur_val
        # if cur_val < self.buy_price * 0.97:
        # SELL, SELL, SELL!!! (with all possible default parameters)
        # self.log('SELL CREATE, %.2f' % self.dataclose[0])

        # Keep track of the created order to avoid a 2nd order
        # self.order = self.sell(size=self.buyCnt)
        # self.order = self.sell()#
        # self.sell(size=1, exectype=bt.Order.StopTrail,
        #          trailpercent=0.02)  # last price will be used as reference


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    labels = []
    for key, value in GlobalVariables.get_stock_data_labels_dict(False).items():
        labels.append(value)

    ##########
    data_in_2 = [
        ('2016-09-30', 23.35, 23.91, 23.24, 23.8, 31800),
        ('2016-10-03', 23.68, 23.69, 23.39, 23.5, 31600),
        ('2016-10-04', 23.52, 23.64, 23.18, 23.28, 31700),
        ('2016-10-05', 23.28, 23.51, 23.27, 23.43, 31500),
        ('2016-10-06', 23.38, 23.56, 23.29, 23.48, 42000),
        ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
        ('2016-10-10', 23.62, 23.88, 23.55, 23.77, 44000),
        ('2016-10-11', 23.62, 23.74, 23.01, 23.16, 45000),
        ('2016-10-12', 26.16, 27, 26.11, 26, 46000),
        ('2016-10-13', 23.52, 23.64, 23.18, 23.238, 32000),
        ('2016-10-14', 23.52, 23.64, 23.18, 23.0, 33000),
        ('2016-10-15', 18.7, 20, 17, 18.5, 33000),
        ('2016-10-16', 18, 19, 16, 15, 33000)]

    df_2 = DataFrame.from_records(data_in_2, columns=labels)
    data_pd_2 = bt.feeds.PandasData(
        dataname=df_2,
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1
    )
    cerebro.adddata(data_pd_2)

    # Set our desired cash start
    cerebro.broker.setcash(P)

    # Set the commission
    # https://www.backtrader.com/docu/commission-schemes/commission-schemes.html
    # 0.5% of the operation value --> 2500 € --> 12.5 per Buy/Sell
    cerebro.broker.setcommission(commission=com)
    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # Run over everything
    cerebro.run()
    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot(style='candlestick', barup='green', bardown='red')

    # TODO thats not the daily returns
    # df = DataFrame.from_records(buy_data, columns=["Date", "StratPrice"])
    # var = value_at_risk(df["StratPrice"], P, c)
    # print("Value-at-Risk: $%0.2f" % var)
