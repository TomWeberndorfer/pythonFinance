# http://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis

# import textblob
# https://banking.einnews.com/sections

# corpus:
# https://nlp.stanford.edu/pubs/lrec2014-stock.pdf
# https://nlp.stanford.edu/pubs/stock-event.html
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import datetime
import pandas as pd


class TextBlobAnalyseNews:
    def __init__(self, names, tickers, threshold=0.7):
        if names is None or tickers is None:
            raise NotImplementedError

        self.classifier = self.__train_classifier()
        self.threshold = threshold
        self.names = names
        self.tickers = tickers

    def analyse_single_news(self, news_to_analyze):
        """
           Analyses a news text and returns a dict with containing data, if news classification is above
           the given threshold (default =0.7)
           :param classifier: news classifier instance
           :param threshold: threshold for classification
           :param news_to_analyze: news text to analyze
           :return: {'name': name_to_find, 'ticker': all_symbols[idx], 'prob_dist': prob_dist,
                     orig_news': str(news_to_analyze), 'translated_news:': str(wiki)}
           """

        if news_to_analyze is None:
            raise NotImplementedError

        result = self.identify_stock_in_news(news_to_analyze)
        if result != " ":
            prob_dist = self.classifier.prob_classify(news_to_analyze)

            if (round(prob_dist.prob("pos"), 2) > self.threshold) or (
                        round(prob_dist.prob("neg"), 2) > self.threshold):
                return {'name': result['name'], 'ticker': result['ticker'], 'prob_dist': prob_dist,
                        'orig_news': str(news_to_analyze)}

        print("ERR: nothing found for news: " + str(news_to_analyze))
        return " "

    def __train_classifier(self):
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
            ('Underperform', 'neg'),

        ]

        train_start = datetime.datetime.now()
        cl = NaiveBayesClassifier(train)
        txt = "\n\nRuntime to train classifier: " + str(datetime.datetime.now() - train_start)
        print(txt)
        return cl

    def identify_stock_in_news(self, news_to_analyze):
        """
        Identifies a stock name within a news and returns the name and ticker
        :param news_to_analyze: news text itself
        :return: {'name': name_to_find, 'ticker': self.tickers[idx]}
                  or " " if no name found
        """

        if news_to_analyze is None:
            raise NotImplementedError

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

                        name_to_find = self.lookup_stock_abr_in_all_names(stock_to_check)
                        if name_to_find != " ":
                            idx = self.names.index(name_to_find)
                            return {'name': name_to_find, 'ticker': self.tickers[idx]}

        print("ERR: nothing found for news: " + str(news_to_analyze))
        return " "

    def lookup_stock_abr_in_all_names(self, stock_abr):
        result = [i for i in self.names if i.lower().startswith(stock_abr.lower())]

        if result:
            name_to_find = str(result[0])
            if name_to_find in self.names:  # TODO: check if this if is necessary
                return name_to_find

        return " "
