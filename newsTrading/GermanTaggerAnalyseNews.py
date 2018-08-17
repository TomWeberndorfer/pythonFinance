# http://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis

# import textblob
# https://banking.einnews.com/sections
import _pickle as pickle

# corpus:
# https://nlp.stanford.edu/pubs/lrec2014-stock.pdf
# https://nlp.stanford.edu/pubs/stock-event.html
import nltk
from textblob.classifiers import NaiveBayesClassifier

from DataRead_Google_Yahoo import get_symbol_and_real_name_from_abbrev_name_from_topforeignstocks
from DataReading.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataReading.StockDataContainer import StockDataContainer
from Utils.common_utils import is_float, GlobalVariables
from Utils.Logger_Instance import logger


class GermanTaggerAnalyseNews:
    def __init__(self, stock_data_container_list, threshold=None, german_tagger=None):
        """
        Init for german tagger class
        :param stock_data_container_list: list with data of stocks as list with class or subclass of StockDataContainer
        :param threshold: classifier threshold to recognize
        :param german_tagger: can be none, and will be loaded otherwise
        """
        # if stock_data_container_list is None:  # TODO: or not isinstance(stock_data_container_list[0], StockDataContainer):
        #    raise NotImplementedError("stock_data_container_list is used wrong")

        self.classifier = self.__train_classifier()
        self.threshold = threshold
        self.stopwords = nltk.corpus.stopwords.words('german')
        self.stock_data_container_list = stock_data_container_list
        self._names = []
        self.tickers = []
        self.stock_exchanges = []

        # TODO statt einzellisten umwandeln glei gscheid
        if self.stock_data_container_list is not None:
            for data_entry in self.stock_data_container_list:
                self._names.append(data_entry.get_stock_name())
                self.tickers.append(data_entry.stock_ticker())
                self.stock_exchanges.append(data_entry.stock_exchange())

        if german_tagger is None or isinstance(german_tagger, str):
            with open(german_tagger, 'rb') as f:
                self.german_tagger = pickle.load(f)
        else:
            self.german_tagger = german_tagger

    def analyse_single_news(self, stock_data_container):
        """
           Analyses a news text and returns a dict with containing data, if news classification is above
           the given threshold (default =0.7)
           :type news_to_analyze: string
           :param stock_data_container: container with news text to analyze
           :return: result_news_stock_data_container
           """

        if stock_data_container is None:
            raise NotImplementedError

        try:
            if stock_data_container.original_news() is not None:
                prob_dist = self.classifier.prob_classify(stock_data_container.original_news())
                stock_data_container.set_prop_dist(prob_dist.prob("pos"))
        except AttributeError:
            # handle missing key
            return None

        return stock_data_container

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
            ('Outperform', 'pos'),
            ('outperform', 'pos'),

            # ('', 'pos'),
            # ('', 'neg')
            ('Share Down', 'neg'),
            ('Target Price Lower', 'neg'),
            ('down', 'neg'),
            ('Down', 'neg'),
            ('lose', 'neg'),
            ('senkt', 'neg'),
            ('belässt', 'neg'),
            ('Sell', 'neg'),
            ('sell', 'neg'),
            ('underperform', 'neg'),
            ('Underperform', 'neg'),
            ('neutral', 'neg'),
            ('Neutral', 'neg'),
            ('reduce', 'neg'),
            ('Reduce', 'neg'),
        ]

        cl = NaiveBayesClassifier(train)
        return cl

    def identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(self,
                                                                                               single_news_to_analyze):
        """
        Identifies a stock name within a news and returns the name and ticker
        :param single_news_to_analyze: news text itself
        :return: {'name': name_to_find, 'ticker': self.tickers[idx]}
                  or " " if no name found
        """

        if single_news_to_analyze is None:
            raise NotImplementedError

        preprocessed_news = self.optimize_text_for_german_tagger(single_news_to_analyze)

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

        noun_tags = ""
        enable_tags = False

        for i in range(len(tags)):
            # TODO gscheider: erst nach dem ersten verb lesen
            if tags[i][1].startswith("V"):
                enable_tags = True
            if enable_tags:
                if tags[i][1].startswith("N"):
                    if i > 1 and tags[i - 1][1].startswith("ADJ"):
                        noun_tags = (tags[i - 1][0] + " " + tags[i][0])
                        break

                    if tags[i][1].startswith("NE") or tags[i][1].startswith("NN"):
                        noun_tags = (tags[i][0])
                        break

        if noun_tags is not None and len(noun_tags) > 0:
            name_return = ""
            target_price_return = 0
            ticker_return = ""
            stock_exchange_return = ""

            stock_to_check = noun_tags  # [0] --> first tag in list
            price_tuple = [i for i in tags if i[1].startswith("CARD")]

            try:
                name_to_find = self.lookup_stock_abr_in_all_names(stock_to_check)
                idx = self._names.index(name_to_find)
                name_return = self._names[idx]
                ticker_return = self.tickers[idx]
                stock_exchange_return = self.stock_exchanges[idx]

            except Exception as e:  # look up symbol in web instead of list
                try:
                    name_return, ticker_return = get_symbol_and_real_name_from_abbrev_name_from_topforeignstocks(
                        stock_to_check)

                except Exception as e:
                    (", No STOCK found for news: " + str(single_news_to_analyze))

                    return None

            if len(price_tuple) > 0:
                price = price_tuple[len(price_tuple) - 1][0]  # TODO 1: comment
                price = price.replace(",", ".")  # replace german comma
                if is_float(price):
                    # price_tuple: [0] --> number, [1]--> CD
                    target_price_return = float(price)

            # news_dec = NewsDataContainerDecorator(StockDataContainer(name_return, ticker_return, stock_exchange_return),
            #                                      target_price_return, "", single_news_to_analyze, 0)

            ret = StockNameTickerExchangeAndTargetPrize(name_return, ticker_return, stock_exchange_return,
                                                        target_price_return)
            return ret

        logger.info("No STOCK found for news: " + str(single_news_to_analyze))
        return None

    def lookup_stock_abr_in_all_names(self, stock_abr, all_names=[]):
        """
        Look up the stock abbreviation in the stock list with _names
        :param stock_abr: abbreviation
        :param all_names: all stock _names list
        :return: name or " "
        """
        if all_names is None or len(all_names) < 1:
            all_names = self._names

        result = [i for i in all_names if i.lower().startswith(stock_abr.lower())]

        if result:
            name_to_find = str(result[0])  # TODO wieso [0]
            if name_to_find in all_names:  # TODO: check if this if is necessary
                return name_to_find

        raise AttributeError("Stock abbr not found: " + str(stock_abr))

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

    def optimize_text_for_german_tagger(self, news_to_analyze):
        """
        Preprocess news for text analysis
        :param news_to_analyze: original news
        :return: preprocessed news
        """
        split_apostrophe = news_to_analyze.split("'")
        for split in split_apostrophe:
            news_to_analyze = news_to_analyze.replace("'" + split + "'", split.lower())

        # tod euronext wird falscherweise ersetzt
        news_to_analyze = news_to_analyze.replace(" Euro", " €")
        news_to_analyze = news_to_analyze.replace(" US-Dollar ", "$")
        news_to_analyze = news_to_analyze.replace(" Dollar ", "$")
        news_to_analyze = news_to_analyze.replace("-", " ")  # TODO with expand_compound_token
        news_to_analyze = news_to_analyze.replace("Ziel", "")  # TODO

        return news_to_analyze


class StockNameTickerExchangeAndTargetPrize:
    def __init__(self, stock_name, stock_ticker, stock_exchange, target_price):
        self._stock_name = stock_name
        self._stock_ticker = stock_ticker
        self._target_price = target_price
        self._stock_exchange = stock_exchange

    def get_stock_name(self):
        return self._stock_name

    def stock_ticker(self):
        return self._stock_ticker

    def stock_exchange(self):
        return self._stock_exchange

    def stock_target_price(self):
        return self._target_price

    def stock_exchange(self):
        return self._stock_exchange
