from Strategies.GapUpHighVolumeStrategy import GapUpHighVolumeStrategy
from Strategies.SimplePatternNewsStrategy import SimplePatternNewsStrategy
from Strategies.Abstract_StrategyFactory import Abstract_StrategyFactory
from Strategies.W52HighTechnicalStrategy import W52HighTechnicalStrategy


class StrategyFactory(Abstract_StrategyFactory):
    def _create_strategy(self, strategy_to_create, stock_data_container_list, parameter_list, all_news_text_list=None):
        strategy = ""

        if strategy_to_create in "SimplePatternNewsStrategy":
            strategy = SimplePatternNewsStrategy(stock_data_container_list, parameter_list, all_news_text_list)

        elif strategy_to_create in "W52HighTechnicalStrategy":
            strategy = W52HighTechnicalStrategy(stock_data_container_list, parameter_list)

        elif strategy_to_create in "GapUpHighVolumeStrategy":
            strategy = GapUpHighVolumeStrategy(stock_data_container_list, parameter_list)

        return strategy
