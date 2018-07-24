import traceback

import bs4 as bs
import datetime
import requests

from DataReading.Abstract_StockDataReader import Abstract_StockDataReader
from Utils.common_utils import print_err_message
from Utils.file_utils import replace_in_file, get_hash_from_file, check_file_exists_or_create, \
    check_file_exists_and_delete
from Utils.news_utils import generate_hash
from datetime import datetime
import pandas as pd


class TraderfoxNewsDataReader(Abstract_StockDataReader):
    def _method_to_execute(self, argument):
        raise NotImplementedError("Not needed because of single thread reading")

    def read_data(self):
        if self.reload_stockdata:
            check_file_exists_and_delete(self.date_file)

        all_news_text_list = self.__read_news_from_traderfox(self.date_file)
        return all_news_text_list

    def __read_news_from_traderfox(self, date_file, date_time_format="%d.%m.%Y um %H:%M"):
        """
        read news from traderfox home page with dpa-afx-compact news
        :param date_time_format: news datetime format
        :param date_file: file for last check date
        :return: news as list
        """
        # TODO enable for enhanced info
        # url = "https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-2-5-8-12/"  # analysen, ad hoc, unternehmen, pflichtmitteilungen
        url = "https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-5/"
        resp = requests.get(url)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        # article --> h2 --> a href for news text, article --> footer for date
        all_articles = soup.find_all("article")

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
                all_news.append(news_text)

        return all_news

    def __is_date_actual(self, date_to_check, last_date_file="", last_date="", date_time_format="%d.%m.%Y um %H:%M"):
        """

        :param date_time_format:
        :type last_date: object
        :param last_date_file:
        :param date_to_check:
        :return:
        """
        try:
            if date_to_check is None:
                raise NotImplementedError

            if last_date == "":
                if check_file_exists_or_create(last_date_file,
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
            print_err_message("Can not check if date is actual.", e, str(traceback.format_exc()))
            return True, ""
