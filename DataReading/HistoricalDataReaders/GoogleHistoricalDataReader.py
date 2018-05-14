from DataReading.StockDataReader import StockDataReader


class GoogleDataReader(StockDataReader):
    def read_data(self):
        pass

    def __init__(self, period, interval, stock_name, date_time_format):
        super().__init__()
        self.start_data = period #TODO
        self.end_date = period  # TODO