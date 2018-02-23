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
    #('', 'pos'),
    #('', 'neg')
    ('Share Down', 'neg'),
    ('Target Price Lower', 'neg'),
     ('Stock Down', 'neg'),
    ('lose', 'neg'),
 ]

test = [
     ('the beer was good.', 'pos'),
     ('I do not enjoy my job', 'neg'),
     ("I ain't feeling dandy today.", 'neg'),
     ("I feel amazing!", 'pos'),
     ('Gary is a friend of mine.', 'pos'),
     ("I can't believe I'm doing this.", 'neg')
 ]


cl = NaiveBayesClassifier(train)

#print(cl.classify("Nvidia shares up nearly 12% premarket after company handily beat with earnings"))

#prob_dist = cl.prob_classify("NVIDIA and AMD Are Losing Gamers to Cryptocurrency Chaos")
#print (round(prob_dist.prob("pos"), 2))

#TODO: vergleich von analystenerwartung und echt (von einnews)

#--------------------------
from newspaper import Article

#url = 'http://finance.yahoo.com/q/h?s=msft'
#url = "https://www.investors.com/etfs-and-funds/etfs/apple-microsoft-amazon-lead-top-growth-stock-play-in-buy-range/?src=A00220&yptr=yahoo"
url = "https://www.investors.com/etfs-and-funds/etfs/apple-microsoft-amazon-lead-top-growth-stock-play-in-buy-range/?src=A00220&yptr=yahoo"
article = Article(url)
article.download()

article.html
article.parse()

print(cl.classify(article.text))