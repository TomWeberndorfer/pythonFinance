from Strategies.SimplePatternNewsStrategy import SimplePatternNewsStrategy
from Strategies.StockScreener import StockScreener


class NewsStrategyFactory(StockScreener):
    def _create_strategy(self, strategy_to_create, num_of_stocks_per_thread, stock_data_container_list, parameter_list):
        strategy = ""

        if strategy_to_create in "SimplePatternNewsStrategy":
            strategy = SimplePatternNewsStrategy(num_of_stocks_per_thread, stock_data_container_list, parameter_list)

        elif strategy_to_create in "W52HighTechnicalStrategy":
            raise NotImplementedError

        return strategy
