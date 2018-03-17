# http://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis

#import textblob
# https://banking.einnews.com/sections

#corpus:
# https://nlp.stanford.edu/pubs/lrec2014-stock.pdf
# https://nlp.stanford.edu/pubs/stock-event.html
from textblob.classifiers import NaiveBayesClassifier

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
print(cl.classify(news))

prob_dist = cl.prob_classify(news)
print (round(prob_dist.prob("pos"), 2))

#TODO: vergleich von analystenerwartung und echt (von einnews)