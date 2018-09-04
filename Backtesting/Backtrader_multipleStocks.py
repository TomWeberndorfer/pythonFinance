from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# import datetime  # For datetime objects
import traceback
from datetime import datetime
from os import listdir
from os.path import isfile, join

# Import the backtrader platform
import backtrader as bt

from Utils.Logger_Instance import logger
from Utils.GlobalVariables import *
from Utils.StockDataUtils import convert_backtrader_to_dataframe

####################################
# https://www.backtrader.com/docu/indautoref.html
#
####################################
# Create a Stratey

program_start_time = datetime.now()


class TestStrategy(bt.Strategy):
    params = (
        ('skipdays', 14),  # skips days to calculate 52week high
        # ('skipdays', 250),  #skips days to calculate 52week high
        ('stockname', "GOOG")
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        # self.dataclose = self.datas[0][GlobalVariables.get_stock_data_labels_dict()['Close']]
        # self.datavol = self.datas[0][GlobalVariables.get_stock_data_labels_dict()['Volume']]
        # self.datahi = self.datas[0][GlobalVariables.get_stock_data_labels_dict()['High']]
        # self.datalo = self.datas[0][GlobalVariables.get_stock_data_labels_dict()['Low']]

        self.dataclose = self.datas[0].close
        self.datavol = self.datas[0].volume
        self.datahi = self.datas[0].high
        self.datalo = self.datas[0].low


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
        self.buyNotAnymore = False

        # Indicators for the plotting show

        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
        #                                     subplot=True)
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.ATR(self.datas[0], plot=False)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):

        # TODO des gscheid machen, nur skip damit man nicht bei der ersten bar anfängt
        # if self.params.skipdays > len(self.dataclose):
        # return

        df1 = convert_backtrader_to_dataframe(self.datas[0])

        # res = strat_52_w_hi_hi_volume(self.params.stockname, df1, 5, 3, 1.2, 0.98)

        # if self.order:
        # return


        # Check if we are in the market
        if not self.position:

            # if res['buy']:
            #     # if raise_cnt < 3:
            #     self.buy_price = self.dataclose[0]
            #     self.log('BUY CREATE, %.2f' % self.dataclose[0])
            #     # Keep track of the created order to avoid a 2nd order
            #     # self.order = self.buy()
            #     self.buyCnt = round((cerebro.broker.cash / self.dataclose[0] / 10))  # TODO
            #     # self.buyCnt = round((cerebro.broker.cash / self.dataclose[0]))-10  # TODO
            #     self.buy(size=self.buyCnt)
            #     # elf.order_target_percent(target = 0.5)

                # --------------------------------------------------
                # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > 1:
                #
                #     # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                #
                #     # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
        # ------------------------------------------------------------
        else:

            cur_val = self.datalo[0]
            if cur_val > self.buy_price:
                self.buy_price = cur_val

            if (cur_val < self.buy_price * 0.96):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell(size=self.buyCnt)
                # self.order_target_percent(target=-0.5)


def get_data_feed(file_path):
    infile = open(file_path, 'r')
    first_line = infile.readline().strip()
    infile.close()

    header = first_line.split(",")

    try:
        o_idx = header.index("Open")
        h_idx = header.index("High")
        l_idx = header.index("Low")
        c_idx = header.index("Close")
        v_idx = header.index("Volume")

        return o_idx, h_idx, l_idx, c_idx, v_idx

    except Exception as e:
        logger.error("Can not get data feed index: " + str(e) + "\n" + str(traceback.format_exc()))
        return


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # datapath = os.path.join(modpath, '../../datas/GOOG.csv')
    # datapath2 = os.path.join(modpath, '../../datas/KMX.csv')

    mypath = 'C:/Users/Tom/OneDrive/Dokumente/Thomas/Aktien/datas/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    for file in onlyfiles:
        dn = 'C:/Users/Tom/OneDrive/Dokumente/Thomas/Aktien/datas/' + file

        o_idx, h_idx, l_idx, c_idx, v_idx = get_data_feed(dn)

        # TODO test für eigenen data reader
        # data = bt.feeds.YahooFinanceCSVData(
        #    dataname=dn,
        #    reverse=False)

        # data = bt.feeds.GenericCSVData(
        #     dataname=dn,
        #     nullvalue=0.0,
        #     dtformat=GlobalVariables.get_stock_data_dtformat(),,
        #     datetime=0,
        #     open=1,
        #     high=2,
        #     low=3,
        #     close=4,
        #     volume=5,
        #     openinterest=-1
        # )

        data = bt.feeds.GenericCSVData(
            dataname=dn,
            nullvalue=0.0,
            dtformat=GlobalVariables.get_stock_data_dtformat(),
            datetime=0,
            open=o_idx,
            high=h_idx,
            low=l_idx,
            close=c_idx,
            volume=v_idx,
            openinterest=-1
        )

        cerebro.adddata(data)

        #TODO: spread

    # Set our desired cash start
    cerebro.broker.setcash(50000.0)

    # Add a FixedSize sizer according to the stake
    # cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # Set the commission
    cerebro.broker.setcommission(commission=0.001)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.addstrategy(TestStrategy)
    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    print("INFO: runtime " + str(
        datetime.now() - program_start_time))

    # Plot the result
    cerebro.plot(style='candlestick', barup='green', bardown='red')
