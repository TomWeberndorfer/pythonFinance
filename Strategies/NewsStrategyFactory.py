from Strategies.SimplePatternNewsStrategy import SimplePatternNewsStrategy
from Strategies.StockScreener import StockScreener


class NewsStrategyFactory(StockScreener):
    def __init__(self, num_of_stocks_per_thread, dataproviders):
        super().__init__(num_of_stocks_per_thread, dataproviders)

    def create_strategy(self, strategy_to_create):
        strategy = ""

        if strategy_to_create in "SimplePatternNewsStrategy":
            strategy = SimplePatternNewsStrategy()

        elif strategy_to_create in "W52HighTechnicalStrategy":
            raise NotImplementedError

        return strategy
