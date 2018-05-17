from DataReading.StockDataReader import StockDataReader


class GoogleHistoricalDataReader(StockDataReader):
    def read_data(self):
        pass

    def __init__(self, period, interval, stock_name, date_time_format):
        super().__init__(period, interval, stock_name, date_time_format)
        self.start_data = period #TODO
        self.end_date = period  # TODO