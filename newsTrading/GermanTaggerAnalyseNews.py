# http://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis

# import textblob
# https://banking.einnews.com/sections

import _pickle as pickle
import datetime
# corpus:
# https://nlp.stanford.edu/pubs/lrec2014-stock.pdf
# https://nlp.stanford.edu/pubs/stock-event.html
import threading
import nltk
from textblob.classifiers import NaiveBayesClassifier

from DataRead_Google_Yahoo import get_symbol_from_name_from_topforeignstocks
from DataReading.NewsStockDataContainer import NewsStockDataContainer
from DataReading.StockDataContainer import StockDataContainer
from MyThread import MyThread
from Utils.common_utils import split_list, is_float


class GermanTaggerAnalyseNews:
    def __init__(self, stock_data_container_list, threshold, german_tagger):
        """
        Init for german tagger class
        :param stock_data_container_list: list with data of stocks as list with class or subclass of StockDataContainer
        :param threshold: classifier threshold to recognize
        :param german_tagger: can be none, and will be loaded otherwise
        """
        if stock_data_container_list is None or not isinstance(stock_data_container_list[0], StockDataContainer):
            raise NotImplementedError("stock_data_container_list is used wrong")

        self.classifier = self.__train_classifier()
        self.threshold = threshold
        self.stopwords = nltk.corpus.stopwords.words('german')
        self.stock_data_container_list = stock_data_container_list
        self.names = []
        self.tickers = []
        self.stock_exchanges = []

        # TODO
        for data_entry in self.stock_data_container_list:
            self.names.append(data_entry.stock_name)
            self.tickers.append(data_entry.stock_ticker)
            self.stock_exchanges.append(data_entry.stock_exchange)

        # self.names = stock_name_list['names']
        # self.tickers = stock_name_list['tickers']
        # self.stock_exchanges = stock_name_list['stock_exchange']

        if german_tagger is None or isinstance(german_tagger, str):
            with open(german_tagger, 'rb') as f:
                self.german_tagger = pickle.load(f)
        else:
            self.german_tagger = german_tagger

    def analyse_single_news(self, news_to_analyze):
        """
           Analyses a news text and returns a dict with containing data, if news classification is above
           the given threshold (default =0.7)
           :param news_to_analyze: news text to analyze
           :return: result_news_stock_data_container
           """

        if news_to_analyze is None:
            raise NotImplementedError

        prep_news = self.__process_news(news_to_analyze)

        result_news_stock_data_container = self._identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(
            prep_news)
        if result_news_stock_data_container != " ":
            prob_dist = self.classifier.prob_classify(prep_news)

            if (round(prob_dist.prob("pos"), 2) > self.threshold) or (
                    round(prob_dist.prob("neg"), 2) > self.threshold):

                result_news_stock_data_container.set_prop_dist(prob_dist)

                #TODO better solution
                for stock_data_container in self.stock_data_container_list:
                    if stock_data_container.stock_ticker == result_news_stock_data_container.stock_ticker:
                        result_news_stock_data_container.set_historical_stock_data(stock_data_container.historical_stock_data)
                        break

                return result_news_stock_data_container

            else:
                print(
                    'BELOW THRESHOLD FOR ' + str(result_news_stock_data_container.stock_name) + ', ticker: ' + str(
                        result_news_stock_data_container.stock_ticker) + ', prob_dist pos: ' + str(
                        round(prob_dist.prob("pos"), 2)) + ', prob_dist neg: ' + str(round(prob_dist.prob("neg"), 2)) +
                    ' orig_news: ' + str(news_to_analyze))

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
            ('outperform', 'pos'),
            ('overweight', 'pos'),

            # ('', 'pos'),
            # ('', 'neg')
            ('Share Down', 'neg'),
            ('Target Price Lower', 'neg'),
            ('Stock Down', 'neg'),
            ('lose', 'neg'),
            ('senkt', 'neg'),
            ('belässt', 'neg'),
            ('Sell', 'neg'),
            ('underperform', 'neg'),
            ('neutral', 'neg'),
            ('reduce', 'neg'),
        ]

        train_start = datetime.datetime.now()
        cl = NaiveBayesClassifier(train)
        print("\nRuntime to train classifier: " + str(datetime.datetime.now() - train_start))
        return cl

    def _identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(self, single_news_to_analyze):
        """
        Identifies a stock name within a news and returns the name and ticker
        :param single_news_to_analyze: news text itself
        :return: {'name': name_to_find, 'ticker': self.tickers[idx]}
                  or " " if no name found
        """

        if single_news_to_analyze is None:
            raise NotImplementedError

        preprocessed_news = self.__process_news(single_news_to_analyze)

        # TODO: http://dsspace.wzb.eu/pyug/text_proc_feature_extraction/
        tokens = nltk.word_tokenize(preprocessed_news, language="german")
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
            name_return = ""
            price_return = 0
            ticker_return = ""
            stock_exchange_return = ""

            noun_idx = len(noun_tag) - 1
            stock_to_check = noun_tag[noun_idx][0]  # [0] --> first tag in list

            name_to_find = self.lookup_stock_abr_in_all_names(stock_to_check)
            price_tuple = [i for i in tags if i[1].startswith("CARD")]

            if name_to_find != " " and name_to_find is not None:
                idx = self.names.index(name_to_find)
                name_return = self.names[idx]
                ticker_return = self.tickers[idx]
                stock_exchange_return = self.stock_exchanges[idx]

            else:  # look up symbol in web instead of list
                name, symbol = get_symbol_from_name_from_topforeignstocks(stock_to_check)
                if symbol is not None and symbol != " " and name is not None and name != " ":
                    name_return = name
                    ticker_return = symbol
                    stock_exchange_return = ""  # TODO 3: return something
                else:
                    return " "  # todo new stockdata container

            if len(price_tuple) > 0:
                price = price_tuple[len(price_tuple) - 1][0]  # TODO 1: comment
                price = price.replace(",", ".")  # replace german comma
                if is_float(price):
                    # price_tuple: [0] --> number, [1]--> CD
                    price_return = float(price)

            return NewsStockDataContainer(name_return, ticker_return, stock_exchange_return, price_return, "",
                                          single_news_to_analyze, 0)
            # TODO price hinzu
            # return {'name': name_return, 'ticker': ticker_return,
            #        'stock_exchange':stock_exchange_return , 'price': price_return}

        print("ERR: no STOCK found for news: " + str(single_news_to_analyze))
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
                news_screening_threads._append_thread(
                    threading.Thread(target=self.__function_for_threading_news_analysis,
                                     kwargs={'news_to_check': curr_news, 'result': result}))

            news_screening_threads._execute_threads()

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

    def __process_news(self, news_to_analyze):
        """
        Preprocess news for text analysis
        :param news_to_analyze: original news
        :return: preprocessed news
        """
        split_apostrophe = news_to_analyze.split("'")
        for split in split_apostrophe:
            news_to_analyze = news_to_analyze.replace("'" + split + "'", split.lower())

        news_to_analyze = news_to_analyze.replace("Euro", "€")
        news_to_analyze = news_to_analyze.replace("US-Dollar", "$")
        news_to_analyze = news_to_analyze.replace("Dollar", "$")
        news_to_analyze = news_to_analyze.replace("-", " ")  # TODO with expand_compound_token

        return news_to_analyze
