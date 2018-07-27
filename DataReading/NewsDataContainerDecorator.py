from DataReading.Abstract_DataContainerDecorcator import Abstract_DataContainerDecorator
from DataReading.StockDataContainer import StockDataContainer


class NewsDataContainerDecorator(Abstract_DataContainerDecorator):

    def __init__(self, shaped_data_container, stock_target_price, prob_dist, original_news,
                 stock_current_prize):
        super().__init__(shaped_data_container)
        self._stock_target_price = stock_target_price
        self._prob_dist = prob_dist
        self._original_news = original_news
        self._stock_current_prize = stock_current_prize

    def get_names_and_values(self):
        names_and_values_dict = self._shaped_data_container.get_names_and_values()

        names_and_values_dict.update(
            {"Target Price": self.stock_target_price(), "Pos. Probability Distribution": self.positive_prob_dist(),
             "Original News": self.original_news(), "Stock Current Prize": self.stock_current_prize()})
        return names_and_values_dict

    def stock_target_price(self):
        return self._stock_target_price

    def positive_prob_dist(self):
        return round(self._prob_dist, 2)

    def original_news(self):
        return self._original_news

    def stock_current_prize(self):
        return self._stock_current_prize

    def set_prop_dist(self, prob_dist):
        self._prob_dist = prob_dist

    def set_stock_target_price(self, stock_target_price):
        self._stock_target_price = stock_target_price