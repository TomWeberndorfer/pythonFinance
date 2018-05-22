from Strategies.SimplePatternNewsStrategy import SimplePatternNewsStrategy
from Strategies.StockScreener import StockScreener
from Strategies.W52HighTechnicalStrategy import W52HighTechnicalStrategy


class NewsStrategyFactory(StockScreener):
    def _create_strategy(self, strategy_to_create, stock_data_container_list, parameter_list):
        strategy = ""

        if strategy_to_create in "SimplePatternNewsStrategy":
            strategy = SimplePatternNewsStrategy(stock_data_container_list, parameter_list)

        elif strategy_to_create in "W52HighTechnicalStrategy":
            strategy = W52HighTechnicalStrategy()

        return strategy
