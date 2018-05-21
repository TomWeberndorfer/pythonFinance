from DataReading.NewsStockDataReaders.DataReaderFactory import DataReaderFactory
from Strategies.Strategy import Strategy
import time
from datetime import datetime

# from DataRead_Google_Yahoo import get_ticker_data_with_webreader
# from Utils.common_utils import format_news_analysis_results, send_stock_email
# from Utils.file_utils import read_tickers_from_file, append_to_file
# from newsFeedReader.traderfox_hp_news import read_news_from_traderfox
from newsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews


class SimplePatternNewsStrategy(Strategy):

    def run_strategy(self, all_news_text_list):
        text_analysis = GermanTaggerAnalyseNews(self.stock_data_container_list, self.parameter_dict['news_threshold'],
                                                self.parameter_dict['german_tagger'])

        # ++++++++++ FOR SAMPLE NEWS
        # data = pd.read_csv(filepath + "Sample_news.txt")
        # all_news = data.News.tolist()

        # all_news.append("ANALYSE-FLASH: NordLB senkt Apple auf 'Kaufen' - Ziel 125,5 Euro")
        # all_news.append("Bryan Garnier hebt Apple auf 'Buy' - Ziel 91 Euro")
        self.result_list = text_analysis.analyse_all_news(all_news_text_list, self.parameter_dict['num_of_stocks_per_thread'])

        return self.result_list
