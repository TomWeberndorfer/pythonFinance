import time
from datetime import datetime

from DataRead_Google_Yahoo import get_ticker_data_with_webreader
from Utils.common_utils import format_news_analysis_results, send_stock_email
from Utils.file_utils import read_tickers_from_file, append_to_file
from newsFeedReader.traderfox_hp_news import read_news_from_traderfox
from newsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews


filepath = 'C:\\temp\\'
tickers_file_name = "stock_tickers.pickle"
stocknames_file_name = "stock_names.pickle"
tickers_file = filepath + tickers_file_name
stocknames_file = filepath + stocknames_file_name
stock_exchange_file_name = "stock_exchange_file.pickle"
stock_exchange_file = filepath + stock_exchange_file_name
res = read_tickers_from_file(tickers_file, stocknames_file, stock_exchange_file)
date_file = "C:\\temp\\last_date_time.csv"
##########################
text_analysis = GermanTaggerAnalyseNews(res)

while True:
    # ++++++++++ FOR SAMPLE NEWS
    # data = pd.read_csv(filepath + "Sample_news.txt")
    # all_news = data.News.tolist()

    all_news = []
    #all_news.append("ANALYSE-FLASH: NordLB senkt Apple auf 'Kaufen' - Ziel 125,5 Euro")
    # all_news.append("Bryan Garnier hebt Apple auf 'Buy' - Ziel 91 Euro")

    thr_start = datetime.now()
    all_news = read_news_from_traderfox(date_file)

    results = text_analysis.analyse_all_news(all_news)

    for single_res in results:
        # get the last available price and compare with rating
        #TODO des is zu langsam
        stock52_w = get_ticker_data_with_webreader(single_res['ticker'], single_res['stock_exchange'], filepath + 'stock_dfs', 'yahoo', False, 1)
        single_res['current_val'] = 0
        if stock52_w is not None and len(stock52_w) > 0:
            current_val = stock52_w.iloc[len(stock52_w) - 1].High
            if current_val:
                single_res['current_val'] = current_val

    res_str = format_news_analysis_results(results)

    if res_str is not None and len(res_str) > 0:
        print(res_str)
        append_to_file(res_str, filepath + "Backtesting.txt") #TODO da ghert a aktuelle abfrage für preis

        send_stock_email(res_str, "News Trading: New news available")
    else:
        print("News analysis: no news")

    time.sleep(60)  # check for new news after x seconds
    print("Runtime check um " + str(datetime.now()) + ": " + str(datetime.now() - thr_start))
