from DataReading.StockDataContainer import StockDataContainer


class NewsStockDataContainer(StockDataContainer):
    def __init__(self, stock_name, stock_ticker, stock_exchange, stock_target_price, prob_dist, orignal_news, stock_current_prize):
        super().__init__(stock_name, stock_ticker, stock_exchange)
        self.stock_target_price = stock_target_price
        self.prob_dist = prob_dist
        self.orignal_news = orignal_news
        self.stock_current_prize = stock_current_prize

    def stock_target_price (self):
        return self.stock_target_price

    def prob_dist (self):
        return self.prob_dist

    def orignal_news(self):
        return self.orignal_news

    def stock_current_prize(self):
        return self.stock_current_prize

    def set_prop_dist(self, prob_dist):
        self.prob_dist = prob_dist

    def set_stock_target_price (self, stock_target_price):
        self.stock_target_price = stock_target_price

    def set_stock_current_prize(self, stock_current_prize):
        self.stock_current_prize = stock_current_prize



