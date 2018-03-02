# http://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis

#import textblob
# https://banking.einnews.com/sections

#corpus:
# https://nlp.stanford.edu/pubs/lrec2014-stock.pdf
# https://nlp.stanford.edu/pubs/stock-event.html
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

from DataRead_Google_Yahoo import get_symbol_from_name_from_yahoo
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

news = "27.02. 16:43 dpa-AFX: ANALYSE-FLASH: DZ Bank hebt Ziel für Airbus auf 116 Euro - 'Kaufen'"
news = "Align Technology"
wiki = TextBlob (news)
print ("noun: " + str(wiki.noun_phrases))
print ("sentiment: " + str(wiki.sentiment))

print(cl.classify(news))

prob_dist = cl.prob_classify(news)
print (round(prob_dist.prob("pos"), 2))

#TODO: vergleich von analystenerwartung und echt (von einnews)

name = get_symbol_from_name_from_yahoo("Airbus")
print (name)
#
filepath = 'C:\\temp\\'
tickers_file_name = "sp500tickers.pickle"
tickers_file = filepath + tickers_file_name

#all_symbols= read_tickers(tickers_file)
all_symbols = read_table_column_from_wikipedia('https://de.wikipedia.org/wiki/Liste_der_im_CDAX_gelisteten_Aktien',
                                               'wikitable sortable zebra', 2)
print (all_symbols)
