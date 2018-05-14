from DataReading.StockDataReader import StockDataReader
import bs4 as bs
import datetime
import requests

from Utils.file_utils import replace_in_file, get_hash_from_file, append_to_file, check_file_exists_or_create
from Utils.news_utils import generate_hash
from datetime import datetime
import pandas as pd


class TraderfoxNewsDataReader(StockDataReader):
    def read_data(self):
        date_file = "C:\\temp\\last_date_time.csv"
        all_news = self.__read_news_from_traderfox(date_file)

        #TODO eventuell newsdatarader geben immer news als liste zur�ck
        return all_news

    def __read_news_from_traderfox(self, date_file, date_time_format="%d.%m.%Y um %H:%M"):
        """
        read news from traderfox home page with dpa-afx-compact news
        :param date_time_format: news datetime format
        :param date_file: file for last check date
        :return: news as list
        """
        # TODO for enhanced
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

        if date_to_check is None:
            raise NotImplementedError

        if last_date == "":
            if check_file_exists_or_create(last_date_file, "last_check_date"):  # no need to check, creates anyway
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

