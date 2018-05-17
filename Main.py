from datetime import time, datetime

from DataRead_Google_Yahoo import get_ticker_data_with_webreader
from Strategies.NewsStrategyFactory import NewsStrategyFactory

#TODO
from Utils.common_utils import format_news_analysis_results, send_stock_email
from Utils.file_utils import append_to_file, FileUtils

try:
    filepath = 'C:\\temp\\'
    stocks_per_threads = 5
    #run_stock_screening(stocks_per_threads)
    stock_data_list = []
    parameter_list = []
    data_provider = "google"  # TODO
    filepath = 'C:\\temp\\'
    stock_list_name = "stockList.txt"
    stock_data_container_file_name = "stock_data_container_file.pickle"
    stock_data_container_file = filepath + stock_data_container_file_name

    stock_data_container_list = FileUtils.read_tickers_from_file(stock_data_container_file)
    thr_start = datetime.now()

    #TODO: alles umstellen auf den container statt listen
    stock_screener = NewsStrategyFactory()
    # prepare_strategy(self, strategy_to_create, num_of_stocks_per_thread, stock_name_list, stock_data_list, parameter_list):
    news_strategy = stock_screener.prepare_strategy("SimplePatternNewsStrategy", stocks_per_threads, stock_data_container_list, parameter_list)
    results = news_strategy.run_strategy()

    # for single_res in results:
    #     # get the last available price and compare with rating
    #     # TODO des is zu langsam
    #     stock52_w = get_ticker_data_with_webreader(single_res['ticker'], single_res['stock_exchange'],
    #                                                filepath + 'stock_dfs', 'yahoo', False, 1)
    #     single_res['current_val'] = 0
    #     if stock52_w is not None and len(stock52_w) > 0:
    #         current_val = stock52_w.iloc[len(stock52_w) - 1].High
    #         if current_val:
    #             single_res['current_val'] = current_val
    #
    # res_str = format_news_analysis_results(results)
    #
    # if res_str is not None and len(res_str) > 0:
    #     print(res_str)
    #     append_to_file(res_str, filepath + "Backtesting.txt")  # TODO da ghert a aktuelle abfrage fuer preis
    #
    #     send_stock_email(res_str, "News Trading: New news available")
    # else:
    #     print("News analysis: no news")
    #
    # time.sleep(60)  # check for new news after x seconds
    # print("Runtime check um " + str(datetime.now()) + ": " + str(datetime.now() - thr_start))

except Exception as e:
    print(str(e))