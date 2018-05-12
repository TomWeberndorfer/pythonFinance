

class StockScreener:
    def __init__(self, num_of_stocks_per_thread, dataproviders):
        self.dataproviders = dataproviders
        self.num_of_stocks_per_thread = num_of_stocks_per_thread

    def run_screening(self, strategy_to_create):
        strategy = self.create_strategy(strategy_to_create)

        #TODO run the strategy
        raise NotImplementedError

    def create_strategy (self, strategy_to_create):
        raise NotImplementedError('TODO')