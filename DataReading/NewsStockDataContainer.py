from DataReading.StockDataContainer import StockDataContainer


class NewsStockDataContainer(StockDataContainer):
    def __init__(self, stock_name, stock_ticker, stock_exchange, stock_price, prob_dist, orignal_news):
        super().__init__(stock_name, stock_ticker, stock_exchange)
        self.stock_price = stock_price
        self.prob_dist = prob_dist
        self.orignal_news = orignal_news

    def stock_price (self):
        return self.stock_price

    def prob_dist (self):
        return self.prob_dist

    def orignal_news(self):
        return self.orignal_news

    def set_prop_dist(self, prob_dist):
        self.prob_dist = prob_dist

