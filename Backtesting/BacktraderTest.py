import backtrader as bt
from datetime import datetime


class TestStrategy(bt.Strategy):
    params = (('percents', 0.9),)  # Float: 1 == 100%

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=21)

    def next(self):
        date = self.data.datetime.date()
        long_stop = self.data.close[0] - 50  # Will not be hit
        short_stop = self.data.close[0] + 50  # Will not be hit
        if not self.position:
            if date == datetime(2018, 1, 11).date():
                # Price closes at $100 and following opens at $100
                # Base test no gapping
                buy_ord = self.order_target_percent(target=self.p.percents)
                buy_ord.addinfo(name="Long Market Entry")
                stop_size = buy_ord.size - abs(self.position.size)
                self.sl_ord = self.sell(size=stop_size, exectype=bt.Order.Stop, price=long_stop)
                self.sl_ord.addinfo(name='Long Stop Loss')
            elif date == datetime(2019, 1, 6).date():
                # Price closes at $100 and following opens at $150
                # Start of first position reversing test
                # Still flat at the moment
                buy_ord = self.order_target_percent(target=self.p.percents)
                buy_ord.addinfo(name="Long Market Entry")
                stop_size = buy_ord.size - abs(self.position.size)
                self.sl_ord = self.sell(size=stop_size, exectype=bt.Order.Stop, price=long_stop)
                self.sl_ord.addinfo(name='Long Stop Loss')
        else:
            # NOTE oco=self.sl_ord is needed to cancel stop losses already in the market
            if date == datetime(2018, 1, 25).date():
                # Price Closes at $140 and following opens at $140
                # Close Tests first - $40 Dollar Profit
                cls_ord = self.close(oco=self.sl_ord)
                cls_ord.addinfo(name="Close Market Order")
            elif date == datetime(2019, 1, 11).date():
                # Price closes at $190 and following opens at $190
                # First Position to Reverse
                # We are selling from net longself. Desired position size
                # Is now net short.
                sell_ord = self.order_target_percent(target=-self.p.percents, oco=self.sl_ord)
                sell_ord.addinfo(name="Short Market Entry")
                stop_size = abs(sell_ord.size) - abs(self.position.size)
                self.sl_ord = self.buy(size=stop_size, exectype=bt.Order.Stop, price=short_stop)
                self.sl_ord.addinfo(name='Short Stop Loss')
            elif date == datetime(2019, 1, 16).date():
                # We are already net short
                # Price closes at $150 and following opens at $150
                # NOTE oco=self.sl_ord is needed to cancel the stop loss already in the market
                # First buy to actually reverse a sell
                buy_ord = self.order_target_percent(target=self.p.percents, oco=self.sl_ord)
                buy_ord.addinfo(name="Long Market Entry")
                stop_size = buy_ord.size - abs(self.position.size)
                self.sl_ord = self.sell(size=stop_size, exectype=bt.Order.Stop, price=long_stop)
                self.sl_ord.addinfo(name='Long Stop Loss')
            elif date == datetime(2019, 1, 21).date():
                # Price closes at $190 and following opens at $190
                # Close to finish
                cls_ord = self.close(oco=self.sl_ord)
                cls_ord.addinfo(name="Close Market Order")

    def notify_order(self, order):
        date = self.data.datetime.datetime().date()

        if order.status == order.Accepted:
            print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
            print('{} Order Accepted'.format(order.info['name']))
            print('{}, Status {}: Ref: {}, Size: {}, Price: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                'NA' if not order.price else round(order.price, 5)
            ))

        if order.status == order.Completed:
            print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
            print('{} Order Completed'.format(order.info['name']))
            print('{}, Status {}: Ref: {}, Size: {}, Price: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                'NA' if not order.price else round(order.price, 5)
            ))
            print('Created: {} Price: {} Size: {}'.format(bt.num2date(order.created.dt), order.created.price,
                                                          order.created.size))
            print('-' * 80)

        if order.status == order.Canceled:
            print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
            print('{} Order Canceled'.format(order.info['name']))
            print('{}, Status {}: Ref: {}, Size: {}, Price: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                'NA' if not order.price else round(order.price, 5)
            ))

        if order.status == order.Rejected:
            print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
            print('WARNING! {} Order Rejected'.format(order.info['name']))
            print('{}, Status {}: Ref: {}, Size: {}, Price: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                'NA' if not order.price else round(order.price, 5)
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


startcash = 10000

# Create an instance of cerebro
cerebro = bt.Cerebro()

# Add our strategy
cerebro.addstrategy(TestStrategy)

# Create a Data Feed
data = bt.feeds.GenericCSVData(
    timeframe=bt.TimeFrame.Days,
    compression=1,
    dataname='C:\\temp\\pythonFinance\\pythonFinance\\DataFiles\\TestData\\TestData.csv',
    nullvalue=0.0,
    dtformat=('%m/%d/%Y'),
    datetime=0,
    time=-1,
    high=2,
    low=3,
    open=1,
    close=4,
    volume=-1,
    openinterest=-1  # -1 means not used
)

# Add the data
cerebro.adddata(data)

# Set our desired cash start
cerebro.broker.setcash(startcash)

# Run over everything
cerebro.run()

# Get final portfolio Value
portvalue = cerebro.broker.getvalue()
pnl = portvalue - startcash

# Print out the final result
print('Final Portfolio Value: ${}'.format(portvalue))
print('P/L: ${}'.format(pnl))
# Finally plot the end results

cerebro.plot(style='candlestick')
