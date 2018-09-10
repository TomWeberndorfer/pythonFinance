import datetime
import traceback
from datetime import datetime

import bs4 as bs
import pandas as pd
import requests

from DataReading.Abstract_StockDataReader import Abstract_StockDataReader
from DataContainerAndDecorator.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Utils.GlobalVariables import *
from Utils.Logger_Instance import logger
from NewsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews


class TraderfoxNewsDataReader(Abstract_StockDataReader):
    def _method_to_execute(self, argument):
        raise NotImplementedError("Not needed because of single thread reading")

    def read_data(self):
        from Utils.FileUtils import FileUtils
        if self.reload_stockdata:
            FileUtils.check_file_exists_and_delete(self._parameter_dict['last_date_time_file'])

        self.__read_news_from_traderfox(self._parameter_dict['last_date_time_file'])

        # TODO returnen
        # return all_news_text_list

    def __read_news_from_traderfox(self, date_file, date_time_format="%d.%m.%Y um %H:%M"):
        """
        read news from traderfox home page with dpa-afx-compact news
        :param date_time_format: news datetime format
        :param date_file: file for last check date
        :return: news as list
        """
        from Utils.FileUtils import FileUtils

        # TODO enable for enhanced info
        # url = "https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-2-5-8-12/"  # analysen, ad hoc, unternehmen, pflichtmitteilungen
        url = "https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-5/"
        resp = requests.get(url)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        # article --> h2 --> a href for news text, article --> footer for date
        all_articles = soup.find_all("article")

        text_analysis = GermanTaggerAnalyseNews(self.stock_data_container_list, None,
                                                self._parameter_dict['german_tagger'])

        # ex: #news = "27.02. 10:41 dpa-AFX: ANALYSE-FLASH: Bryan Garnier hebt Morphosys auf 'Buy' - Ziel 91 Euro"
        all_news = []
        last_date = ""
        for elm in all_articles:
            date_time = (str(elm.footer.span.get_text()))  # date and Time
            date_time = date_time.rsplit(' Uhr')[0]  # TODO: split because of datetime format
            datetime_object = datetime.strptime(date_time, date_time_format)
            is_a_new_news, last_date = self.__is_date_actual(datetime_object, date_file, last_date)

            if is_a_new_news:
                article_text = (str(elm.h2.get_text(strip=True)))  # h2 --> article head line
                news_text = date_time.replace(',', '.') + ", " + article_text.replace(',', '.')
                # TODO irgendwann wegdoa
                FileUtils.append_textline_to_file(news_text,
                                                  GlobalVariables.get_data_files_path() + "NewsForBacktesting.txt",
                                                  True)
                all_news.append(news_text)
                # TODO des ist doppelt, auch im identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier
                prep_news = text_analysis.optimize_text_for_german_tagger(news_text)
                name_ticker_exchange_target_prize = \
                    text_analysis.identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(
                        news_text)
                if name_ticker_exchange_target_prize is not None and name_ticker_exchange_target_prize.get_stock_name() != "":
                    container = StockDataContainer(name_ticker_exchange_target_prize.get_stock_name(),
                                                   name_ticker_exchange_target_prize.stock_ticker(),
                                                   name_ticker_exchange_target_prize.stock_exchange())

                    if container in self.stock_data_container_list:
                        idx = self.stock_data_container_list.index(container)
                        container_2 = self.stock_data_container_list[idx]
                        if isinstance(container_2, StockDataContainer):
                            container = container_2
                            self.stock_data_container_list.remove(container_2)

                    news_dec = NewsDataContainerDecorator(container,
                                                          name_ticker_exchange_target_prize.stock_target_price(),
                                                          0, prep_news)

                    self.stock_data_container_list.append(news_dec)

        # TODO mal was returnen
        # return all_news

    def __is_date_actual(self, date_to_check, last_date_file="", last_date="", date_time_format="%d.%m.%Y um %H:%M"):
        """

        :param date_time_format:
        :type last_date: object
        :param last_date_file:
        :param date_to_check:
        :return:
        """
        from Utils.FileUtils import FileUtils
        try:
            if date_to_check is None:
                raise NotImplementedError

            if last_date == "":
                if FileUtils.check_file_exists_or_create(last_date_file,
                                               "last_check_date" + "\n01.01.2000 um 00:00"):  # no need to check, creates anyway
                    data = pd.read_csv(last_date_file)
                    last_date_str = str(data.last_check_date[0])
                    last_date = datetime.strptime(last_date_str, date_time_format)
                else:
                    return False, ""

            is_news_current = last_date < date_to_check

            if is_news_current:
                with open(last_date_file, "w") as myfile:
                    myfile.write("last_check_date" + "\n")
                    datetime_object_str = datetime.strftime(date_to_check, date_time_format)
                    myfile.write(str(datetime_object_str) + "\n")
                    return is_news_current, date_to_check

            return is_news_current, last_date

        except Exception as e:
            logger.error("Exception Can not check if date is actual.: " + str(e) + "\n" + str(traceback.format_exc()))
            return True, ""
