from Strategies.SimplePatternNewsStrategy import SimplePatternNewsStrategy
from Strategies.StockScreener import StockScreener


class NewsStrategyFactory(StockScreener):
    def _create_strategy(self, strategy_to_create, stock_name_list, stock_data_list, parameter_list):
        strategy = ""

        if strategy_to_create in "SimplePatternNewsStrategy":
            strategy = SimplePatternNewsStrategy(stock_name_list, stock_data_list, parameter_list)

        elif strategy_to_create in "W52HighTechnicalStrategy":
            raise NotImplementedError

        return strategy
