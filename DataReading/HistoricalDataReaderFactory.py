from StockScreener import StockScreener


class HistoricalDataReaderFacotry (StockScreener):

    def read_data(self):
        raise NotImplementedError('TODO')

    def get_symbol_from_name (self):
        raise NotImplementedError('TODO')