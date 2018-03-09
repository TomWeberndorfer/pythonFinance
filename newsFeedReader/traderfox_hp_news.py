import bs4 as bs
import datetime
import requests

from Utils.file_utils import replace_in_file, get_hash_from_file, append_to_file, check_file_exists_or_create
from Utils.news_utils import generate_hash
from datetime import datetime
import pandas as pd


def read_news_from_traderfox(hash_file):
    """
    Read the news from traderfox homepage with html parsing to "articles"
    :param hash_file filepath+name  for hash id
    :return: news as list
    """
    # TODO
    # url = "https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-2-5-8-12/"  # analysen, ad hoc, unternehmen, pflichtmitteilungen
    url = "https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-5/"
    date_time_format = "%d.%m.%Y um %H:%M"
    date_file = "C:\\temp\\last_date_time.csv"

    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    # article --> h2 --> a href for news text, article --> footer for date
    all_articles = soup.find_all("article")

    # TODO reactivate hash maybe, if read all news to slow
    # last_id = get_hash_from_file(hash_file, url)
    # hash_id = generate_hash(url, all_articles)
    # if last_id == hash_id:
    #    print("no news")
    #    return ""
    # else:

    # ex: #news = "27.02. 10:41 dpa-AFX: ANALYSE-FLASH: Bryan Garnier hebt Morphosys auf 'Buy' - Ziel 91 Euro"
    all_news = []
    last_date = ""
    # replace_in_file(hash_file, last_id, hash_id)
    for elm in all_articles:
        date_time = (str(elm.footer.span.get_text()))  # date and Time
        date_time = date_time.rsplit(' Uhr')[0]
        datetime_object = datetime.strptime(date_time, date_time_format)
        is_a_new_news, last_date = is_date_actual(datetime_object, date_file, last_date)

        if is_a_new_news:
            article_text = (str(elm.h2.get_text(strip=True)))  # h2 --> article head line
            news_text = date_time.replace(',', '.') + ", " + article_text.replace(',', '.')
            append_to_file(news_text, "C:\\temp\\Traderfox_News.csv")  # TODO only for first data example collection
            all_news.append(news_text)

    return all_news


def is_date_actual(date_to_check, last_date_file="", last_date="", date_time_format="%d.%m.%Y um %H:%M"):
    """

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

    is_news_current= last_date < date_to_check

    if is_news_current:
        with open(last_date_file, "w") as myfile:
            myfile.write("last_check_date" + "\n")
            datetime_object_str = datetime.strftime(date_to_check, date_time_format)
            myfile.write(str(datetime_object_str) + "\n")
            return is_news_current, date_to_check

    return is_news_current, last_date
