from Strategies.StockScreener import StockScreener


class HistoricalDataReaderFactory (StockScreener):

    def _create_strategy(self, strategy_to_create):
        pass

    def read_data(self):
        raise NotImplementedError('TODO')

    def get_symbol_from_name (self):
        raise NotImplementedError('TODO')