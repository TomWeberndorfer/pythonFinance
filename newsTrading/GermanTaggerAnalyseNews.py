# http://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis

# import textblob
# https://banking.einnews.com/sections

# corpus:
# https://nlp.stanford.edu/pubs/lrec2014-stock.pdf
# https://nlp.stanford.edu/pubs/stock-event.html
import threading

import _pickle as pickle

import nltk
from textblob_de import TextBlobDE as TextBlob
import textblob_de as textblob
from textblob.classifiers import NaiveBayesClassifier

# TODO
# from textblob import TextBlob
import datetime
import pandas as pd

from MyThread import MyThread
from Utils.common_utils import split_list
from Utils.file_utils import read_tickers_from_file

filepath = 'C:\\temp\\'
tickers_file_name = "stock_tickers.pickle"
stocknames_file_name = "stock_names.pickle"
tickers_file = filepath + tickers_file_name
stocknames_file = filepath + stocknames_file_name
hash_file = filepath + "news_hashes.txt"


##########################

class GermanTaggerAnalyseNews:
    def __init__(self, names=None, tickers=None, threshold=0.7, german_tagger=None):
        self.classifier = self.__train_classifier()
        self.threshold = threshold
        self.stopwords = nltk.corpus.stopwords.words('german')

        if german_tagger is None:
            with open('C:\\temp\\nltk_german_classifier_data.pickle', 'rb') as f:
                self.german_tagger = pickle.load(f)
        else:
            self.german_tagger = german_tagger

        if names is None or tickers is None:
            res = read_tickers_from_file(tickers_file, stocknames_file)
            self.names = res['names']
            self.tickers = res['tickers']
        else:
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

        result = self.identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news_to_analyze)
        if result != " ":
            prob_dist = self.classifier.prob_classify(news_to_analyze)

            if (round(prob_dist.prob("pos"), 2) > self.threshold) or (
                    round(prob_dist.prob("neg"), 2) > self.threshold):
                return {'name': result['name'], 'ticker': result['ticker'], 'prob_dist': prob_dist,
                        'orig_news': str(news_to_analyze), 'price': result['price']}

            else:
                print(
                    'BELOW THRESHOLD FOR ' + str(result['name']) + ', ticker: ' + str(
                        result['ticker']) + ', prob_dist pos: ' + str(
                        round(prob_dist.prob("pos"), 2)) + ', prob_dist neg: ' + str(round(prob_dist.prob("neg"), 2)) +
                    'orig_news' + str(news_to_analyze))

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
            ('empfiehlt', 'pos'),

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
        print("\nRuntime to train classifier: " + str(datetime.datetime.now() - train_start))
        return cl

    def identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(self, news_to_analyze):
        """
        Identifies a stock name within a news and returns the name and ticker
        :param news_to_analyze: news text itself
        :return: {'name': name_to_find, 'ticker': self.tickers[idx]}
                  or " " if no name found
        """

        if news_to_analyze is None:
            raise NotImplementedError

        split_apostrophe = news_to_analyze.split("'")
        for split in split_apostrophe:
            news_to_analyze = news_to_analyze.replace("'" + split + "'", split.lower())

        news_to_analyze = news_to_analyze.replace("Euro", "€")
        news_to_analyze = news_to_analyze.replace("Dollar", "$")
        news_to_analyze = news_to_analyze.replace("-", " ")  # TODO with expand_compound_token

        # TODO: http://dsspace.wzb.eu/pyug/text_proc_feature_extraction/
        tokens = nltk.word_tokenize(news_to_analyze, language="german")
        tokens_removed_words = [t for t in tokens if t.lower() not in self.stopwords]

        # http: // dsspace.wzb.eu / pyug / text_proc_feature_extraction /
        # tmp_tokens = {}
        # for doc_label, doc_tok in tokens_removed_words:
        #     tmp_tokens[doc_label] = []
        #     for t in doc_tok:
        #         t_parts = self.expand_compound_token(t)
        #         tmp_tokens[doc_label].extend(t_parts)

        tags = self.german_tagger.tag(tokens_removed_words)

        noun_tag = [i for i in tags if i[1].startswith("NE")]

        if noun_tag is not None and len(noun_tag) > 0:
            noun_idx = len(noun_tag) - 1
            stock_to_check = noun_tag[noun_idx][0]  # [0] --> first tag in list

            name_to_find = self.lookup_stock_abr_in_all_names(stock_to_check)
            price_tuple = [i for i in tags if i[1].startswith("CARD")]

            if name_to_find != " " and name_to_find is not None:
                idx = self.names.index(name_to_find)

                if len(price_tuple) > 0:
                    price = price_tuple[0][0]
                    # price_tuple: [0] --> number, [1]--> CD
                    return {'name': name_to_find, 'ticker': self.tickers[idx],
                            'price': price}

                else:
                    return {'name': name_to_find, 'ticker': self.tickers[idx],
                            'price': 0}

        print("ERR: no STOCK found for news: " + str(news_to_analyze))
        return " "

    def lookup_stock_abr_in_all_names(self, stock_abr):
        """
        Look up the stock abbreviation in the stock list with names
        :param stock_abr: abbrevation
        :return: name or " "
        """
        result = [i for i in self.names if i.lower().startswith(stock_abr.lower())]

        if result:
            name_to_find = str(result[0])  # TODO wieso [0]
            if name_to_find in self.names:  # TODO: check if this if is necessary
                return name_to_find

        return " "

    def __function_for_threading_news_analysis(self, news_to_check, result):
        print("Started with: " + str(news_to_check))

        for news in news_to_check:
            res_analysis = self.analyse_single_news(news)

            if res_analysis != " ":
                result.append(res_analysis)

    def analyse_all_news(self, all_news, num_of_news_per_thread=2):

        result = []

        if all_news != "" and len(all_news) >= 1:
            news_screening_threads = MyThread("news_screening_threads")
            splits = split_list(all_news, num_of_news_per_thread)

            for curr_news in splits:
                news_screening_threads.append_thread(
                    threading.Thread(target=self.__function_for_threading_news_analysis,
                                     kwargs={'news_to_check': curr_news, 'result': result}))

            news_screening_threads.execute_threads()

        return result

    def expand_compound_token(t, split_chars="-"):
        parts = []
        add = False  # signals if current part should be appended to previous part
        for p in t.split(split_chars):  # for each part p in compound token t
            if not p: continue  # skip empty part
            if add and parts:  # append current part p to previous part
                parts[-1] += p
            else:  # add p as separate token
                parts.append(p)
            add = len(p) <= 1  # if p only consists of a single character -> append the next p to it
            # add = p.isupper()   # alt. strategy: if p is all uppercase ("US", "E", etc.) -> append the next p to it

        return parts
