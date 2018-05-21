from datetime import datetime

import os

from DataRead_Google_Yahoo import get_ticker_data_with_webreader

from DataReading.NewsStockDataReaders.DataReaderFactory import DataReaderFactory
from DataReading.StockDataContainer import StockDataContainer
from Strategies.NewsStrategyFactory import NewsStrategyFactory

#TODO
from Utils.common_utils import CommonUtils
from Utils.file_utils import FileUtils

#try:
from Utils.news_utils import NewsUtils

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#TODO ev in config file -->  gui load
filepath = ROOT_DIR + '\\DataFiles\\'
stocks_per_threads = 5
source='yahoo'
weeks_delta=52
#run_stock_screening(stocks_per_threads)
stock_data_list = []
parameter_dict = {'news_threshold': 0.7, 'german_tagger': filepath + 'nltk_german_classifier_data.pickle', 'num_of_stocks_per_thread': 2}
# params for strat_52_w_hi_hi_volume
w52hi_parameter_dict = {'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98, 'num_of_stocks_per_thread': 5}
data_provider = "google"  # TODO
stock_list_name = "stockList.txt"
stock_data_container_file_name = "stock_data_container_file.pickle"
stock_data_container_file = filepath + stock_data_container_file_name

# TODO- eini verschieben irgendwo, ned manuell
#TODO muss die strategie schon de daten griagn? ja schon, wanns mehrere san kinan ned alle wieder lesen

stock_data_container_list = FileUtils.read_tickers_from_file(stock_data_container_file)
#TODO abstract factory: http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html
data_storage = DataReaderFactory()
#TODO eventuell als return statt als call by reference: stock_data_container_list = data_storage.read_data("GoogleHistoricalDataReader", stock_data_container_list, weeks_delta, filepath + 'stock_dfs')
stock_data_reader = data_storage.prepare("GoogleHistoricalDataReader")


# TODO 10: disabled zu langsam ohne threading
#stock_data_reader.read_data(stock_data_container_list, weeks_delta, filepath + 'stock_dfs', source)

news_data_storage = DataReaderFactory()
news_stock_data_reader = news_data_storage.prepare("traderfox_hp_news")
all_news_text_list = news_stock_data_reader.read_data(filepath + "last_date_time.csv")

#-----------------
#TODO while True:
thr_start = datetime.now()
stock_screener = NewsStrategyFactory()
# prepare_strategy(self, strategy_to_create, num_of_stocks_per_thread, stock_name_list, stock_data_list, parameter_dict):
news_strategy = stock_screener.prepare_strategy("SimplePatternNewsStrategy", stocks_per_threads, stock_data_container_list, parameter_dict)
results = news_strategy.run_strategy(all_news_text_list)

for single_res in results:
    # get the last available price and compare with rating
    # TODO des is zu langsam
    #TODO: in de historical steht nix drin bis jetzt --> kein join, 2 verschiedne container

    stock52_w = single_res.historical_stock_data
    current_val  = 0
    if stock52_w is not None and len(stock52_w) > 0:
        current_val = stock52_w.iloc[len(stock52_w) - 1].High

    single_res.set_stock_current_prize(current_val)

res_str = NewsUtils.format_news_analysis_results(results)

if res_str is not None and len(res_str) > 0:
    print()
    print ('------------------------')
    print(res_str)
    FileUtils.append_to_file(res_str, filepath + "Backtesting.txt")  # TODO da ghert a aktuelle abfrage fuer preis
    #TODO CommonUtils.send_stock_email(res_str, "News Trading: New news available")
else:
    print("News analysis: no news")

#time.sleep(60)  # check for new news after x seconds
print("Runtime check um " + str(datetime.now()) + ": " + str(datetime.now() - thr_start))

#except Exception as e:
   # print(str(e))