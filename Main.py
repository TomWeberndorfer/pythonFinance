import os
from datetime import datetime
from DataReading.NewsStockDataReaders.DataReaderFactory import DataReaderFactory
from Strategies.StrategyFactory import NewsStrategyFactory
from Utils.file_utils import FileUtils, read_tickers_from_file
from Utils.news_utils import NewsUtils

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# TODO ev in config file -->  gui load
filepath = ROOT_DIR + '\\DataFiles\\'
data_source = 'yahoo'
weeks_delta = 52  # one year in the past

parameter_dict = {'news_threshold': 0.7, 'german_tagger': filepath + 'nltk_german_classifier_data.pickle'}
w52hi_parameter_dict = {'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98}
stock_data_container_file_name = "stock_data_container_file.pickle"
stock_data_container_file = filepath + stock_data_container_file_name

stock_data_container_list = read_tickers_from_file(stock_data_container_file)
# TODO abstract factory: http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html
# TODO eventuell als return statt als call by reference: stock_data_container_list = data_storage.read_data("HistoricalDataReader", stock_data_container_list, weeks_delta, filepath + 'stock_dfs')
# TODO relead data
data_storage = DataReaderFactory()
stock_data_reader = data_storage.prepare("HistoricalDataReader")
# TODO 10
# stock_data_reader.read_data(stock_data_container_list, weeks_delta, stock_data_container_file, data_source,
#                            reload_stockdata=True)

news_data_storage = DataReaderFactory()
news_stock_data_reader = news_data_storage.prepare("TraderfoxNewsDataReader")

# TODO auch hier parallel
all_news_text_list = news_stock_data_reader.read_data(filepath + "last_date_time.csv")

thr_start = datetime.now()
stock_screener = NewsStrategyFactory()
news_strategy = stock_screener.prepare_strategy("SimplePatternNewsStrategy", stock_data_container_list, parameter_dict)
results = news_strategy.run_strategy(all_news_text_list)

# TODO 10:
import os
os.remove("C:\\temp\\pythonFinance\\pythonFinance\\DataFiles\\last_date_time.csv")

if 1:
        stock_data_reader.read_data(results, weeks_delta, stock_data_container_file, data_source,
                                   reload_stockdata=True)

        # todo 10 des stimmt garned zaum zwischen current price und was er wirklich is
        for data in results:
                if len(data.historical_stock_data) > 0:
                    data.set_stock_current_prize(data.historical_stock_data.High[len(results) -1])
                else:
                    print("ERROR: failed load hist data for " + data.stock_name)

res_str = NewsUtils.format_news_analysis_results(results)

if res_str is not None and len(res_str) > 0:
    print()
    print ('------------------------')
    print(res_str)
    #FileUtils.append_to_file(res_str, filepath + "Backtesting.txt")  # TODO da ghert a aktuelle abfrage fuer preis
    #TODO CommonUtils.send_stock_email(res_str, "News Trading: New news available")
else:
    print("News analysis: no news")

#time.sleep(60)  # check for new news after x seconds
print("Runtime check um " + str(datetime.now()) + " und dauer: " + str(datetime.now() - thr_start))
