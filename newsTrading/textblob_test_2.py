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
from Utils.common_utils import read_table_column_from_wikipedia
from Utils.file_utils import read_tickers_from_file

filepath = 'C:\\temp\\'
tickers_file_name = "stock_tickers.pickle"
stocknames_file_name = "stock_names.pickle"
tickers_file = filepath + tickers_file_name
stocknames_file = filepath + stocknames_file_name
all_symbols = []
all_names = []


#class TextBlobAnalyseNews:
    #def __init__(self, name):
        #TODO


def analyse_single_news(news_to_analyze, classifier, threshold=0.7):
    """
       Analyses a news text and returns a dict with containing data, if news classification is above
       the given threshold (default =0.7)
       :param classifier: news classifier instance
       :param threshold: threshold for classification
       :param news_to_analyze: news text to analyze
       :return: {'name': name_to_find, 'ticker': all_symbols[idx], 'prob_dist': prob_dist,
                 orig_news': str(news_to_analyze), 'translated_news:': str(wiki)}
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
                            prob_dist = classifier.prob_classify(news_to_analyze)
                            # print("name: " + name_to_find + ", idx: " + str(idx) + ", ticker: " + str(
                            #    all_symbols[idx]) + ", pos: " + str(round(prob_dist.prob("pos"), 2)) + " ,neg: " + str(
                            #    round(prob_dist.prob("neg"), 2)) + ", orig_news: " + str(news_to_analyze) + ", translated news: "+ str(wiki))

                            if (round(prob_dist.prob("pos"), 2) > threshold) or (
                                        round(prob_dist.prob("neg"), 2) > threshold):
                                return {'name': name_to_find, 'ticker': all_symbols[idx], 'prob_dist': prob_dist,
                                        'orig_news': str(news_to_analyze), 'translated_news:': str(wiki)}

                                # return prob_dist #TODO des is blödsinn
                                # else:
                                # any other news- ex: "02.03.18, Airbus erwägt Lager-​Aufstockung wegen Brexit"
                                # TODO
                                # print ("ERROR other tags are not implemented: " + str(tag))

    print("ERR: nothing found for news: " + str(news_to_analyze))
    return " "


def train_classifier():
    """
    Trains the classifier due to given data
    :return: classifier
    """

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
        ('lifts', 'pos'),

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
    txt = "\n\nRuntime to train classifier: " + str(datetime.datetime.now() - thr_start)
    print(txt)
    return cl


thr_start = datetime.datetime.now()
all_news = []
data = pd.read_csv(filepath + "Sample_news.txt")
# ex: #news = "27.02. 10:41 dpa-AFX: ANALYSE-FLASH: Bryan Garnier hebt Morphosys auf 'Buy' - Ziel 91 Euro"

all_news.extend(data.News)
res = read_tickers_from_file(tickers_file, stocknames_file)
all_symbols.extend(res['tickers'])
all_names.extend(res['names'])
class_1 = train_classifier()
results = []

for news in all_news:
    r = analyse_single_news(news, class_1, 0.7)
    results.append(r)

print("\n-------------------------\n")
for res in results:
    if res != " ":
        print("pos: " + str(round(res['prob_dist'].prob("pos"), 2)) + " ,neg: " + str(
            round(res['prob_dist'].prob("neg"), 2)) + " " + str(res))

txt = "\n\nRuntime : " + str(datetime.datetime.now() - thr_start)
print(txt)
