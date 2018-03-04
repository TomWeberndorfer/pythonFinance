import bs4 as bs
import requests

link = "https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-2-5-8/" #analysen, ad hoc, unternehmen

resp = requests.get(link)
soup = bs.BeautifulSoup(resp.text, 'lxml')

#TODO instead of h2: article --> h2 --> a href
for elm in soup.find_all("h2"):
    print (str(elm.get_text(strip=True)))