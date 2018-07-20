from DataReading.Abstract_DataContainerDecorcator import Abstract_DataContainerDecorator
from DataReading.StockDataContainer import StockDataContainer


class NewsDataContainerDecorator(Abstract_DataContainerDecorator):

    def __init__(self, shaped_data_container, stock_target_price, prob_dist, original_news,
                 stock_current_prize):
        super().__init__(shaped_data_container)
        self.stock_target_price = stock_target_price
        self.prob_dist = prob_dist
        self.original_news = original_news
        self.stock_current_prize = stock_current_prize

    def get_names_and_values(self):
        names_and_values_dict = self.shaped_data_container.get_names_and_values()

        names_and_values_dict.update({"Target Price": self.stock_target_price, "Probability Distribution": self.prob_dist, "Original News": self.original_news, "Stock Current Prize": self.stock_current_prize})
        return names_and_values_dict


    def stock_target_price(self):
        return self.stock_target_price

    def prob_dist(self):
        return self.prob_dist

    def orignal_news(self):
        return self.original_news

    def stock_current_prize(self):
        return self.stock_current_prize

    def set_prop_dist(self, prob_dist):
        self.prob_dist = prob_dist

    def set_stock_target_price(self, stock_target_price):
        self.stock_target_price = stock_target_price
