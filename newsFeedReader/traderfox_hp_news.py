import bs4 as bs
import requests


from Utils.common_utils import append_to_file
from Utils.file_utils import replace_in_file, get_hash_from_file, append_to_file
from Utils.news_utils import generate_hash

url = "https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-2-5-8-12/"  # analysen, ad hoc, unternehmen, pflichtmitteilungen
hash_file = "C:\\temp\\news_hashes.txt"

last_id = get_hash_from_file(hash_file, url)
# http://www.pythonforbeginners.com/python-on-the-web/beautifulsoup-4-python/
resp = requests.get(url)
soup = bs.BeautifulSoup(resp.text, 'lxml')

# article --> h2 --> a href for news text, article --> footer for date
all_articles = soup.find_all("article")
id = generate_hash(url, all_articles)
print(id)

if last_id == id:
    print("no news")

else:

    replace_in_file("C:\\temp\\news_hashes.txt", last_id, id)
    for elm in all_articles:
        date_time = (str(elm.footer.get_text(strip=True)))  # date and Time
        article_text = (str(elm.h2.get_text(strip=True)))  # h2 --> article head line
        append_to_file(date_time + ", " + article_text, "C:\\temp\\Traderfox_News.csv")
