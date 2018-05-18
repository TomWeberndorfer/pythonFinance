from datetime import datetime

from DataRead_Google_Yahoo import get_ticker_data_with_webreader
from Strategies.NewsStrategyFactory import NewsStrategyFactory

#TODO
from Utils.common_utils import CommonUtils
from Utils.file_utils import FileUtils

#try:
from Utils.news_utils import NewsUtils

filepath = 'C:\\temp\\'
stocks_per_threads = 5
#run_stock_screening(stocks_per_threads)
stock_data_list = []
parameter_dict = {'news_threshold': 0.7, 'german_tagger': 'C:\\temp\\nltk_german_classifier_data.pickle', 'num_of_stocks_per_thread': 2}
# params for strat_52_w_hi_hi_volume
w52hi_parameter_dict = {'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98, 'num_of_stocks_per_thread': 5}
data_provider = "google"  # TODO
filepath = 'C:\\temp\\'
stock_list_name = "stockList.txt"
stock_data_container_file_name = "stock_data_container_file.pickle"
stock_data_container_file = filepath + stock_data_container_file_name

stock_data_container_list = FileUtils.read_tickers_from_file(stock_data_container_file)
stock_screener = NewsStrategyFactory()

#TODO while True:
thr_start = datetime.now()
# prepare_strategy(self, strategy_to_create, num_of_stocks_per_thread, stock_name_list, stock_data_list, parameter_dict):
news_strategy = stock_screener.prepare_strategy("SimplePatternNewsStrategy", stocks_per_threads, stock_data_container_list, parameter_dict)
results = news_strategy.run_strategy()

for single_res in results:
    # get the last available price and compare with rating
    # TODO des is zu langsam

    stock52_w = get_ticker_data_with_webreader(single_res.stock_ticker, single_res.stock_exchange,
                                            filepath + 'stock_dfs', 'yahoo', False, 1)
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