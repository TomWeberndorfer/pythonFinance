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

#TODO
#from textblob import TextBlob
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

class TextBlobAnalyseNews:
    def __init__(self, names=None, tickers=None, threshold=0.7):
        self.classifier = self.__train_classifier()
        self.threshold = threshold

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

        result = self.identify_stock_and_price_from_news_textblob(news_to_analyze)
        if result != " ":
            prob_dist = self.classifier.prob_classify(news_to_analyze)

            if (round(prob_dist.prob("pos"), 2) > self.threshold) or (
                    round(prob_dist.prob("neg"), 2) > self.threshold):
                return {'name': result['name'], 'ticker': result['ticker'], 'prob_dist': prob_dist,
                        'orig_news': str(news_to_analyze), 'price': result['price']}

            else:
                print(
                    'BELOW THRESHOLD FOR ' + str(result['name']) + 'ticker' + str(result['ticker']) + 'prob_dist' + str(
                        prob_dist) +
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

    def identify_stock_and_price_from_news_textblob(self, news_to_analyze):
        """
        Identifies a stock name within a news and returns the name and ticker
        :param news_to_analyze: news text itself
        :return: {'name': name_to_find, 'ticker': self.tickers[idx]}
                  or " " if no name found
        """

        if news_to_analyze is None:
            raise NotImplementedError

        wiki = TextBlob(news_to_analyze)
        languages = ["de"] #, "en"]  # TODO
        #https: // pypi.python.org / pypi / textblob - de

        for lang in languages:
            #TODO
            #if lang not in wiki.detect_language():
                #wiki = (wiki.translate(from_lang=wiki.detect_language(), to='en'))

            tags = wiki.tags

            # VB means verb --> the noun next to the verb is the stock name
            # ex: Bryan Garnier hebt Morphosys auf 'Buy' - Ziel 91 Euro
            # TODO if "ANALYSE-FLASH" in tag:
            # tag explanaition: https://www.clips.uantwerpen.be/pages/MBSP-tags
            vb_tag = [i for i in tags if i[1].startswith("VB")]

            if vb_tag is not None and len(vb_tag) > 0:
                tag_idx = tags.index(vb_tag[0])  # [0] --> first tag in list

                if len(tags) > tag_idx + 1 + 1:  # TODO beschreiben
                    stock_to_check = tags[tag_idx + 1][0]

                    name_to_find = self.lookup_stock_abr_in_all_names(stock_to_check)
                    price_tuple = [i for i in tags if i[1].startswith("CD")]

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

    def identify_stock_and_price_from_news_nltk_german_classifier_data(self, news_to_analyze, german_tagger):
        """
        Identifies a stock name within a news and returns the name and ticker
        :param news_to_analyze: news text itself
        :return: {'name': name_to_find, 'ticker': self.tickers[idx]}
                  or " " if no name found
        """

        if news_to_analyze is None:
            raise NotImplementedError

        tags = german_tagger.tag(TextBlob(news_to_analyze).words)

        # VB means verb --> the noun next to the verb is the stock name
        # ex: Bryan Garnier hebt Morphosys auf 'Buy' - Ziel 91 Euro
        # TODO if "ANALYSE-FLASH" in tag:
        # tag explanaition: https://www.clips.uantwerpen.be/pages/MBSP-tags
        vb_tag = [i for i in tags if i[1].startswith("VAFIN") or i[1].startswith("VVFIN")]

        if vb_tag is not None and len(vb_tag) > 0:
            tag_idx = tags.index(vb_tag[0])  # [0] --> first tag in list

            if len(tags) > tag_idx + 1 + 1:  # TODO beschreiben
                stock_to_check = tags[tag_idx + 1][0]

                name_to_find = self.lookup_stock_abr_in_all_names(stock_to_check)
                price_tuple = [i for i in tags if i[1].startswith("CD")]

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

    def identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(self, news_to_analyze, german_tagger):
        """
        Identifies a stock name within a news and returns the name and ticker
        :param news_to_analyze: news text itself
        :return: {'name': name_to_find, 'ticker': self.tickers[idx]}
                  or " " if no name found
        """

        if news_to_analyze is None:
            raise NotImplementedError

        news_to_analyze = news_to_analyze.replace ("'", "")
        news_to_analyze = news_to_analyze.replace("Underperform", "unterdurchschnittlich")
        news_to_analyze = news_to_analyze.replace("Euro", "€")
        news_to_analyze = news_to_analyze.replace("Dollar", "$")#

        # TODO: http://dsspace.wzb.eu/pyug/text_proc_feature_extraction/
        tokens = nltk.word_tokenize(news_to_analyze, language="german")
        stopwords = nltk.corpus.stopwords.words('german')
        tokens_removed_words = [t for t in tokens if t.lower() not in stopwords]
        tags = german_tagger.tag(tokens_removed_words)

        # VB means verb --> the noun next to the verb is the stock name
        # ex: Bryan Garnier hebt Morphosys auf 'Buy' - Ziel 91 Euro
        # TODO if "ANALYSE-FLASH" in tag:
        # tag explanaition: https://www.clips.uantwerpen.be/pages/MBSP-tags
        #TODO noun_tag = [i for i in tags if i[1].startswith("NN") or i[1].startswith("NE")]
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
