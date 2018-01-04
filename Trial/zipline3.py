import pytz
from datetime import datetime, timedelta
import zipline
from zipline.api import order, record, symbol
from zipline.algorithm import TradingAlgorithm
#from zipline.utils.factory import load_bars_from_yahoo
from DataRead_Google_Yahoo import read_data_from_google_with_pandas, read_data_from_google_with_client

end_date = datetime.now()
start_date = (end_date - timedelta(weeks=52))
#stock_data = read_data_from_google_with_pandas("AAPL", start_date, end_date)

data = read_data_from_google_with_client("AAPL")

def initialize(context):
    pass

def handle_data(context, data):
    order(symbol('AAPL'), 10)
    record(AAPL=data[symbol('AAPL')].price)


algo_obj = TradingAlgorithm(initialize=initialize,
handle_data=handle_data)
perf_manual = algo_obj.run(data)