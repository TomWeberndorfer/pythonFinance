from DataReading.NewsStockDataReaders.NewsDataReaderFactory import NewsDataReaderFactory
from Strategies.Strategy import Strategy
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
news_threshold = 0.5
##########################

class SimplePatternNewsStrategy (Strategy):

    def run_strategy(self):
        #TODO parameter aus self statt da oben
        results = []
        text_analysis = GermanTaggerAnalyseNews(self.stock_name_list, news_threshold)

        # ++++++++++ FOR SAMPLE NEWS
        # data = pd.read_csv(filepath + "Sample_news.txt")
        # all_news = data.News.tolist()

        all_news = []
        # all_news.append("ANALYSE-FLASH: NordLB senkt Apple auf 'Kaufen' - Ziel 125,5 Euro")
        # all_news.append("Bryan Garnier hebt Apple auf 'Buy' - Ziel 91 Euro")
        data_storage = NewsDataReaderFactory()
        data_storage.read() TODO hier
        all_news = read_news_from_traderfox(date_file) #TODO in basis klasse?
        results = text_analysis.analyse_all_news(all_news)

        return results



