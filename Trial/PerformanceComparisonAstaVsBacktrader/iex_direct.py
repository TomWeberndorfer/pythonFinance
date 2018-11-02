from iexfinance import get_historical_data
from datetime import datetime
from Utils.Abstract_SimpleMultithreading import Abstract_SimpleMultithreading
from abc import abstractmethod


class IexDirect(Abstract_SimpleMultithreading):

    @abstractmethod
    def _method_to_execute(self, symbol):
        start_time = datetime.now()
        start = datetime(2017, 2, 9)
        end = datetime(2017, 5, 24)

        # iex = 1, 0 = quandl
        if 1:
            df = get_historical_data(symbol, start=start, end=end, output_format='pandas')

        else:
            import quandl
            auth_tok = 'Gq6_HqRdHa8KWKV4r7-F'
            start_time = datetime.now()
            df = quandl.get("WIKI/AAPL", trim_start="2014-12-12", trim_end="2014-12-30", authtoken=auth_tok)

        # print("Time to get the stock " + symbol+ ":" + (str(datetime.now() - start_time)))
        return df

    def read_data(self, symbols):
        """
        Read the data and return stock data container list
        :return: stock data container list
        """
        test = self.map_list(symbols)

        return test


if __name__ == '__main__':

    for i in range(0, 5):
        symbols = ["AAPL", "FB", "GIS", "GE", "XOM"]
        start_time = datetime.now()

        iex = IexDirect()
        res = iex.read_data(symbols)
        print(str((str(datetime.now() - start_time))))
        # print("ALL TIME: " + (str(datetime.now() - start_time)))
    print()
