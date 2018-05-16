
class StockDataContainer:
    def __init__(self, stock_name, stock_ticker, stock_exchange):
        self.stock_exchange = stock_exchange
        self.stock_name = stock_name
        self.stock_ticker = stock_ticker

    #@property
    def stock_exchange(self):
        return self.stock_exchange

    #@property
    def stock_name(self):
        return self.stock_name

    #@property
    def stock_ticker(self):
        return self.stock_ticker
