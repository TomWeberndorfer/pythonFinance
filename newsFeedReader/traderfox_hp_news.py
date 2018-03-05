import bs4 as bs
import requests

from Utils.file_utils import replace_in_file, get_hash_from_file, append_to_file
from Utils.news_utils import generate_hash


def read_news_from_traderfox(hash_file):
    """
    Read the news from traderfox homepage with html parsing to "articles"
    :param hash_file filepath+name  for hash id
    :return: news as list
    """
    url = "https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-2-5-8-12/"  # analysen, ad hoc, unternehmen, pflichtmitteilungen

    last_id = get_hash_from_file(hash_file, url)
    # http://www.pythonforbeginners.com/python-on-the-web/beautifulsoup-4-python/
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')

    # article --> h2 --> a href for news text, article --> footer for date
    all_articles = soup.find_all("article")
    hash_id = generate_hash(url, all_articles)

    if last_id == hash_id:
        print("no news")
        return ""

    else:
        # ex: #news = "27.02. 10:41 dpa-AFX: ANALYSE-FLASH: Bryan Garnier hebt Morphosys auf 'Buy' - Ziel 91 Euro"
        all_news = []
        replace_in_file(hash_file, last_id, hash_id)
        for elm in all_articles:
            date_time = (str(elm.footer.get_text(strip=True)))  # date and Time
            article_text = (str(elm.h2.get_text(strip=True)))  # h2 --> article head line
            news_text = date_time + ", " + article_text
            append_to_file(news_text, "C:\\temp\\Traderfox_News.csv") #TODO only for first data example collection
            all_news.append(news_text)

        return all_news

