# http://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis

# import textblob
# https://banking.einnews.com/sections

# corpus:
# https://nlp.stanford.edu/pubs/lrec2014-stock.pdf
# https://nlp.stanford.edu/pubs/stock-event.html
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import traceback
import datetime
import sys

import pandas as pd

from DataRead_Google_Yahoo import __get_symbol_from_name_from_yahoo
from Utils import read_tickers, read_table_column_from_wikipedia

filepath = 'C:\\temp\\'
tickers_file_name = "stock_tickers.pickle"
stocknames_file_name = "stock_names.pickle"
tickers_file = filepath + tickers_file_name
stocknames_file = filepath + stocknames_file_name
all_symbols = []
all_names = []


def analyse_news(news_to_analyze):
    """
       TODO
       :param news_to_analyze:
       :param languages:
       :return:
       """

    wiki = TextBlob(news_to_analyze)
    languages = ["de", "en"]  # TODO

    for lang in languages:
        if lang not in wiki.detect_language():
            wiki = (wiki.translate(from_lang=wiki.detect_language(), to='en'))

        tags = wiki.tags

        # TODO if "ANALYSE-FLASH" in tag:
        for tag in tags:
            # VB means verb --> the noun next to the verb is the stock name
            # ex: Bryan Garnier hebt Morphosys auf 'Buy' - Ziel 91 Euro
            if "VB" in tag[1]:  # ex: <class 'tuple'>: ('lifts', 'VBZ')
                tag_idx = tags.index(tag)
                if len(tags) > tag_idx + 1 + 1:  # TODO beschreiben
                    stock_to_check = tags[tag_idx + 1][0]
                    result = [i for i in all_names if i.lower().startswith(stock_to_check.lower())]

                    if result:
                        name_to_find = str(result[0])

                        if name_to_find in all_names:
                            idx = all_names.index(name_to_find)
                            prob_dist = cl.prob_classify(news_to_analyze)
                            # print("name: " + name_to_find + ", idx: " + str(idx) + ", ticker: " + str(
                            #    all_symbols[idx]) + ", pos: " + str(round(prob_dist.prob("pos"), 2)) + " ,neg: " + str(
                            #    round(prob_dist.prob("neg"), 2)) + ", orig_news: " + str(news_to_analyze) + ", translated news: "+ str(wiki))

                            return {'name': name_to_find, 'ticker': all_symbols[idx], 'prob_dist': prob_dist,
                                    'orig_news': str(news_to_analyze), 'translated_news:': str(wiki)}

                            # return prob_dist #TODO des is blödsinn
                            # else:
                            # any other news- ex: "02.03.18, Airbus erwägt Lager-​Aufstockung wegen Brexit"
                            # TODO
                            # print ("ERROR other tags are not implemented: " + str(tag))

    print("ERR: nothing found for news: " + str(news_to_analyze))
    return " "


# "Main"
train = [
    ('Share Up', 'pos'),
    ('Sale Up', 'pos'),
    ('Target Price Raise', 'pos'),
    ('Production Raise', 'pos'),
    ('Stock Up', 'pos'),
    ('Business Expand', 'pos'),
    ('hebt', 'pos'),
    ('kaufen', 'pos'),
    ('buy', 'pos'),

    # ('', 'pos'),
    # ('', 'neg')
    ('Share Down', 'neg'),
    ('Target Price Lower', 'neg'),
    ('Stock Down', 'neg'),
    ('lose', 'neg'),
    ('senkt', 'neg'),
    ('belässt', 'neg'),
    ('Sell', 'neg'),
]

thr_start = datetime.datetime.now()
cl = NaiveBayesClassifier(train)

news_list = []
data = pd.read_csv(filepath + "Sample_news.txt")
# ex: #news = "27.02. 10:41 dpa-AFX: ANALYSE-FLASH: Bryan Garnier hebt Morphosys auf 'Buy' - Ziel 91 Euro"
news_list.extend(data.News)

res = read_tickers(tickers_file, stocknames_file)
all_symbols.extend(res['tickers'])
all_names.extend(res['names'])

results = []
for news in news_list:
    r = analyse_news(news)
    results.append(r)

print("\n-------------------------\n")
for res in results:
    if res != " ":
        print("pos: " + str(round(res['prob_dist'].prob("pos"), 2)) + " ,neg: " + str(
            round(res['prob_dist'].prob("neg"), 2)) + " " + str(res))
print("end")
