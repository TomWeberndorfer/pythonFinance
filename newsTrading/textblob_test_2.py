# http://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis

#import textblob
# https://banking.einnews.com/sections

#corpus:
# https://nlp.stanford.edu/pubs/lrec2014-stock.pdf
# https://nlp.stanford.edu/pubs/stock-event.html
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

from DataRead_Google_Yahoo import __get_symbol_from_name_from_yahoo
from Utils import read_tickers, read_table_column_from_wikipedia

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

    #('', 'pos'),
    #('', 'neg')
    ('Share Down', 'neg'),
    ('Target Price Lower', 'neg'),
     ('Stock Down', 'neg'),
    ('lose', 'neg'),
    ('belässt', 'neg'),
    ('Sell', 'neg'),
 ]

cl = NaiveBayesClassifier(train)

#news = "27.02. 16:43 dpa-AFX: ANALYSE-FLASH: DZ Bank hebt Ziel für Airbus auf 116 Euro - 'Kaufen'"
#news = "27.02. 16:08 dpa-AFX: ANALYSE-FLASH: DZ Bank hebt MTU Aero Engines auf 'Kaufen' - Fairer Wert 166 Euro"
news = "27.02. 09:51 dpa-AFX: ANALYSE-FLASH: Liberum belässt Aixtron auf 'Buy' - 'Ausblick vorsichtig'"

# news = "Align Technology"
wiki = TextBlob (news)
#print ("noun: " + str(wiki.noun_phrases))
# print ("sentiment: " + str(wiki.sentiment))
#
# print(cl.classify(news))
#
# prob_dist = cl.prob_classify(news)
# print (round(prob_dist.prob("pos"), 2))

#TODO: vergleich von analystenerwartung und echt (von einnews)

filepath = 'C:\\temp\\'
tickers_file_name = "stock_tickers.pickle"
stocknames_file_name = "stock_names.pickle"
tickers_file = filepath + tickers_file_name
stocknames_file = filepath + stocknames_file_name
all_symbols = []
all_names = []

symbol = __get_symbol_from_name_from_yahoo("IFA Hotel & Touristik AG", "de")
symbol = __get_symbol_from_name_from_yahoo ("BMW AG", "de")

res = read_tickers(tickers_file, stocknames_file)
all_symbols.extend(res['tickers'])
all_names.extend(res['names'])

#result = [i for i in all_names if "mtu" in i.lower()]

for noun in wiki.noun_phrases:
    result = [i for i in all_names if i.lower().startswith(noun)]

    if result:
        name_to_find = str(result [0])

        if name_to_find in all_names:
            idx= all_names.index(name_to_find)
            print("idx: " + str(idx))
            print ("ticker: " + str(all_symbols[idx]))
            print(cl.classify(news))
            prob_dist = cl.prob_classify(news)
            print (round(prob_dist.prob("pos"), 2))
            break

print ("end")