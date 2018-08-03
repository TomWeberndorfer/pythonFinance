import unittest
from datetime import datetime

from pandas import DataFrame

from DataRead_Google_Yahoo import get_symbol_and_real_name_from_abbrev_name_from_topforeignstocks
from DataReading.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataReading.StockDataContainer import StockDataContainer
from Utils.GlobalVariables import *
from newsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\TestData\\'


class TestGermanTaggerAnalyseNews(unittest.TestCase):

    def test_analyse_single_news(self):
        rwe_cont = NewsDataContainerDecorator(StockDataContainer("RWE AG ST O.N.", "RWE", "de"), 0, 0,
                                              "ANALYSE-FLASH: Credit Suisse nimmt RWE mit 'Outperform' wieder auf", 0)
        rwe_cont2 = NewsDataContainerDecorator(StockDataContainer("RWE AG ST O.N.", "RWE", "de"), 0, 0,
                                               "19.03.2018 um 08:58, ANALYSE-FLASH: HSBC senkt RWE auf 'Reduce' - Ziel 18 Euro",
                                               0)
        rhm = StockDataContainer("RHEINMETALL AG", "RHM", "de")
        bei = StockDataContainer("BEIERSDORF AG O.N.", "BEI", "de")
        ads = StockDataContainer("ADIDAS AG NA O.N.", "ADS", "de")
        aapl = NewsDataContainerDecorator(StockDataContainer("Apple Inc.", "AAPL", "en"), 0, 0,
                                          "ANALYSE-FLASH: Credit Suisse nimmt Apple mit 'Underperform' wieder auf", 0)
        aapl2 = NewsDataContainerDecorator(StockDataContainer("Apple Inc.", "AAPL", "en"), 0, 0,
                                           "ANALYSE-FLASH: Independent Research senkt Ziel für Apple auf 118 Euro", 0)
        aapl3 = NewsDataContainerDecorator(StockDataContainer("Apple Inc.", "AAPL", "en"), 0, 0,
                                           "05.03.2018, ANALYSE-FLASH: NordLB hebt Apple auf 'Kaufen' - Ziel 125 Euro",
                                           0)
        acx = StockDataContainer("BET-AT-HOME.COM AG O.N.", "ACX", "de")
        rhhby = StockDataContainer("Roche Holding AG", "RHHBY", "")
        lor = StockDataContainer("LOrealfuture", "LORFK8.EX", "")

        stock_data_container_list = [rwe_cont, rwe_cont2, rhm, bei, ads, aapl, acx, rhhby, lor, aapl2, aapl3]

        analysis = GermanTaggerAnalyseNews(stock_data_container_list, 0.7,
                                           GlobalVariables.get_data_files_path() + 'nltk_german_classifier_data.pickle')

        result = analysis.analyse_single_news(rwe_cont)
        t1 = round(result.positive_prob_dist(), 2)
        self.assertEqual("RWE AG ST O.N.", result.get_stock_name())
        self.assertEqual("RWE", result.stock_ticker())
        self.assertGreater(t1, 0.7)

        result = analysis.analyse_single_news(rwe_cont2)
        t1 = round(result.positive_prob_dist(), 2)
        self.assertEqual(result.get_stock_name(), "RWE AG ST O.N.")
        self.assertEqual("RWE", result.stock_ticker())
        self.assertGreater(0.7, t1)

        result = analysis.analyse_single_news(aapl)
        t1 = round(result.positive_prob_dist(), 2)
        self.assertEqual(result.get_stock_name(), "Apple Inc.")
        self.assertEqual("AAPL", result.stock_ticker())
        self.assertGreater(0.7, t1)

        result = analysis.analyse_single_news(aapl2)
        t1 = round(result.positive_prob_dist(), 2)
        self.assertEqual(result.get_stock_name(), "Apple Inc.")
        self.assertEqual("AAPL", result.stock_ticker())
        self.assertGreater(0.7, t1)

        result = analysis.analyse_single_news(aapl3)
        t1 = round(result.positive_prob_dist(), 2)
        self.assertEqual("AAPL", result.stock_ticker())
        self.assertGreater(t1, 0.7)

    def test_analyse_single_news_CDAX_companies(self):
        rhm = NewsDataContainerDecorator(StockDataContainer("RHEINMETALL AG", "RHM", "de"), 0, 0,
                                         "05.03.2018, ANALYSE-FLASH: NordLB hebt Rheinmetall auf 'Kaufen' - Ziel 125 Euro",
                                         0)
        bei = NewsDataContainerDecorator(StockDataContainer("BEIERSDORF AG O.N.", "BEI", "de"), 0, 0,
                                         "ANALYSE-FLASH: Independent Research senkt Ziel für Beiersdorf auf 118 Euro",
                                         0)
        ads = NewsDataContainerDecorator(StockDataContainer("ADIDAS AG NA O.N.", "ADS", "de"), 0, 0,
                                         "ANALYSE-FLASH: Credit Suisse nimmt Adidas mit 'Underperform' wieder auf", 0)
        # acx = NewsDataContainerDecorator(StockDataContainer("BET-AT-HOME.COM AG O.N.", "ACX", "de"), 0, 0,
        # , 0
        # rhhby = NewsDataContainerDecorator(StockDataContainer("Roche Holding AG", "RHHBY", "")
        # lor = NewsDataContainerDecorator(StockDataContainer("LOrealfuture", "LORFK8.EX", "")

        stock_data_container_list = [rhm, bei, ads]  # TODO, acx, rhhby, lor]

        analysis = GermanTaggerAnalyseNews(stock_data_container_list, 0.7,
                                           GlobalVariables.get_data_files_path() + 'nltk_german_classifier_data.pickle')

        # CDAX companies
        result = analysis.analyse_single_news(ads)
        t1 = round(result.positive_prob_dist(), 2)
        self.assertGreater(0.7, t1)
        self.assertEqual(result.get_stock_name(), "ADIDAS AG NA O.N.")
        self.assertEqual(result.stock_ticker(), "ADS")

        result = analysis.analyse_single_news(bei)
        t1 = round(result.positive_prob_dist(), 2)
        self.assertGreater(0.7, t1)
        self.assertEqual(result.get_stock_name(), "BEIERSDORF AG O.N.")
        self.assertEqual("BEI", result.stock_ticker())

        result = analysis.analyse_single_news(rhm)
        t1 = round(result.positive_prob_dist(), 2)
        self.assertGreater(t1, 0.7)
        self.assertEqual(result.get_stock_name(), "RHEINMETALL AG")
        self.assertEqual("RHM", result.stock_ticker())

        # news = "DZ Bank empfiehlt Sixt-Aktie nach starken Geschäftszahlen zum Kauf"
        # result = analysis.analyse_single_news(news)
        # t1 = round(result.positive_prob_dist(), 2)
        # self.assertGreater(t1, 0.7)
        #
        # # should fail and return " "
        # news = "01.03.2018, Das sagen Ökonomen zur bevorstehenden Wahl in Italien"
        # result = analysis.analyse_single_news(news)
        # self.assertEqual(True, result is None)
        #
        # news = "17.03.2018 um 09:05, PROSIEBENSAT.1 IM FOKUS: Dax-Absteiger stellt Weichen für bessere Zeiten"
        # result = analysis.analyse_single_news(news)
        # self.assertEqual(True, result is None)

    def test_identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(self):
        stock_data_container_list = [StockDataContainer("RWE AG ST O.N.", "RWE", "de"),
                                     StockDataContainer("RHEINMETALL AG", "RHM", "de"),
                                     StockDataContainer("BEIERSDORF AG O.N.", "BEI", "de"),
                                     StockDataContainer("ADIDAS AG NA O.N.", "ADS", "de"),
                                     StockDataContainer("Apple Inc.", "AAPL", "en"),
                                     StockDataContainer("BET-AT-HOME.COM AG O.N.", "ACX", "de"),
                                     StockDataContainer("Roche Holding AG", "RHHBY", ""),
                                     StockDataContainer("LOrealfuture", "LORFK8.EX", "")]

        analysis = GermanTaggerAnalyseNews(stock_data_container_list, 0.7,
                                           GlobalVariables.get_data_files_path() + 'nltk_german_classifier_data.pickle')

        news = " ANALYSE FLASH: NordLB senkt Ziel für Deutsche Bank auf 11.50 €   halten"  #
        result = analysis.identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(news)
        self.assertEqual(result.get_stock_name(), "Deutsche Bank Aktiengesellschaft")
        self.assertEqual("DB", result.stock_ticker())
        self.assertEqual("", result.stock_exchange())
        self.assertEqual(11.5, result.stock_target_price())

        news = "ANALYSE-FLASH: Jefferies hebt Ziel für RWE auf 250 US-Dollar - 'Underperform'"
        result = analysis.identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(news)
        self.assertEqual(result.get_stock_name(), "RWE AG ST O.N.")
        self.assertEqual("RWE", result.stock_ticker())
        self.assertEqual("de", result.stock_exchange())
        self.assertEqual(250, result.stock_target_price())

        # no price --> 0
        news = "19.03.2018 um 08:21, ANALYSE-FLASH: Credit Suisse nimmt RWE mit 'Outperform' wieder auf"
        result = analysis.identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(news)
        self.assertEqual(result.get_stock_name(), "RWE AG ST O.N.")
        self.assertEqual("RWE", result.stock_ticker())
        self.assertEqual("de", result.stock_exchange())
        self.assertEqual(0, result.stock_target_price())

        news = "ANALYSE-FLASH: Credit Suisse nimmt Rheinmetall mit 'Underperform' wieder auf"
        result = analysis.identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(news)
        self.assertEqual(result.get_stock_name(), "RHEINMETALL AG")
        self.assertEqual("RHM", result.stock_ticker())
        self.assertEqual("de", result.stock_exchange())
        self.assertEqual(0, result.stock_target_price())

        # price with german coma, should also be possible
        news = "ANALYSE-FLASH: Independent Research senkt Ziel für Beiersdorf auf 118,7 Euro"
        result = analysis.identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(news)
        self.assertEqual(result.get_stock_name(), "BEIERSDORF AG O.N.")
        self.assertEqual("BEI", result.stock_ticker())
        self.assertEqual("de", result.stock_exchange())
        self.assertEqual(118.7, result.stock_target_price())

        # price with english comma
        news = "ANALYSE-FLASH: Independent Research senkt Ziel für Beiersdorf auf 118.7 Euro"
        result = analysis.identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(news)
        self.assertEqual("BEIERSDORF AG O.N.", result.get_stock_name())
        self.assertEqual("BEI", result.stock_ticker())
        self.assertEqual("de", result.stock_exchange())
        self.assertEqual(118.7, result.stock_target_price())

        news = "ANALYSE-FLASH: Credit Suisse nimmt Adidas mit 'Underperform' wieder auf"
        result = analysis.identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(news)
        self.assertEqual(result.get_stock_name(), "ADIDAS AG NA O.N.")
        self.assertEqual("de", result.stock_exchange())
        self.assertEqual("ADS", result.stock_ticker())

        news = "ANALYSE-FLASH: NordLB hebt Apple auf 'Kaufen' - Ziel 125 Dollar"
        result = analysis.identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(news)
        self.assertEqual("Apple Inc.", result.get_stock_name())
        self.assertEqual("AAPL", result.stock_ticker())
        self.assertEqual("en", result.stock_exchange())
        self.assertEqual(125, result.stock_target_price())

        news = "Credit Suisse nimmt RWE mit 'Outperform' wieder auf"
        result = analysis.identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(news)
        self.assertEqual(result.get_stock_name(), "RWE AG ST O.N.")
        self.assertEqual("RWE", result.stock_ticker())
        self.assertEqual("de", result.stock_exchange())
        self.assertEqual(0, result.stock_target_price())

        news = "ANALYSE-FLASH: Hauck & Aufhäuser senkt Bet-at-home auf 'Hold' - Ziel 89 Euro"
        result = analysis.identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(news)
        self.assertEqual('BET-AT-HOME.COM AG O.N.', result.get_stock_name())
        self.assertEqual("ACX", result.stock_ticker())
        self.assertEqual("de", result.stock_exchange())
        self.assertEqual(89, result.stock_target_price())

        # not in stock list --> read stock tickers and _names from webservice
        news = "Goldman belässt Roche auf conviction buy list"
        result = analysis.identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(news)
        self.assertEqual('Roche Holding AG', result.get_stock_name())
        self.assertEqual("RHHBY", result.stock_ticker())
        self.assertEqual("", result.stock_exchange())
        self.assertEqual(0, result.stock_target_price())

        news = "Jefferies senkt Ziel für Loreal auf 186 euro Hold"
        result = analysis.identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(news)
        self.assertEqual(result.get_stock_name(), 'LOrealfuture')
        # TODO des ändeert se imma: - LORFM8.EX oder LORFK8.EX
        #  self.assertEqual(result._stock_ticker, "LORFK8.EX")
        self.assertEqual("", result.stock_exchange())
        self.assertEqual(186, result.stock_target_price())

        news = "senkt Ziel für auf 186 euro"
        result = analysis.identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(news)
        self.assertEqual(True, result is None)

    def test_analyse_single_news_with_all_params(self):
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [('2016-09-13', 23.6, 23.73, 23.15, 23.26, 31000),
                ('2016-09-14', 23.33, 23.43, 22.95, 23.11, 31000),
                ('2016-09-15', 23.15, 23.77, 23.14, 23.62, 31000),
                ('2016-09-16', 23.57, 23.68, 23.38, 23.5, 31000)]

        df = DataFrame.from_records(data, columns=labels)
        rwe_container = NewsDataContainerDecorator(StockDataContainer("RWE AG ST O.N.", "RWE", "de"), 0, 0,
                                                   "20.07.2018 um 08:02, ANALYSE-FLASH: Morgan Stanley hebt RWE auf \\'Overweight\\' und Ziel auf 26 Euro",
                                                   0)
        rwe_container.set_historical_stock_data(df)

        stock_data_container_list = [rwe_container,
                                     StockDataContainer("RHEINMETALL AG", "RHM", "de"),
                                     StockDataContainer("BEIERSDORF AG O.N.", "BEI", "de"),
                                     StockDataContainer("ADIDAS AG NA O.N.", "ADS", "de"),
                                     StockDataContainer("Apple Inc.", "AAPL", "en"),
                                     StockDataContainer("BET-AT-HOME.COM AG O.N.", "ACX", "de"),
                                     StockDataContainer("Roche Holding AG", "RHHBY", ""),
                                     StockDataContainer("LOrealfuture", "LORFK8.EX", "")]

        analysis = GermanTaggerAnalyseNews(stock_data_container_list, 0.7,
                                           GlobalVariables.get_data_files_path() + 'nltk_german_classifier_data.pickle')

        result = analysis.analyse_single_news(rwe_container)
        t1 = round(result.positive_prob_dist(), 2)
        self.assertEqual("RWE AG ST O.N.", result.get_stock_name())
        self.assertEqual("RWE", result.stock_ticker())
        self.assertEqual("de", result.stock_exchange())
        self.assertEqual({}, result.get_recommendation_strategies())
        self.assertGreater(t1, 0.7)

    def test_get_symbol_from_name_from_topforeignstocks(self):
        # TODO 1:
        name, symbol = get_symbol_and_real_name_from_abbrev_name_from_topforeignstocks("Nestle")

        name, symbol = get_symbol_and_real_name_from_abbrev_name_from_topforeignstocks("Roche")
        self.assertEqual(name, 'Roche Holding AG')

        if "RHHBY" in symbol:
            # TODO
            self.assertEqual(symbol, "RHHBY")
        else:
            self.assertEqual(symbol, "ROG.VX")

        # name, symbol = get_symbol_and_real_name_from_abbrev_name_from_topforeignstocks("Tesla")
        # self.assertEqual(symbol, "TSLA")
        # self.assertEqual(name, 'Tesla, Inc.')

    def test_lookup_stock_abr_in_all_names(self):
        stock_data_container_list = [StockDataContainer("RWE AG ST O.N.", "RWE", "de"),
                                     StockDataContainer("RHEINMETALL AG", "RHM", "de"),
                                     StockDataContainer("BEIERSDORF AG O.N.", "BEI", "de"),
                                     StockDataContainer("ADIDAS AG NA O.N.", "ADS", "de"),
                                     StockDataContainer("Apple Inc.", "AAPL", "en"),
                                     StockDataContainer("BET-AT-HOME.COM AG O.N.", "ACX", "de"),
                                     StockDataContainer("Roche Holding AG", "RHHBY", ""),
                                     StockDataContainer("LOrealfuture", "LORFK8.EX", "")]

        analysis = GermanTaggerAnalyseNews(stock_data_container_list, 0.7,
                                           filepath + 'nltk_german_classifier_data.pickle')

        result = analysis.lookup_stock_abr_in_all_names("Rheinmetall")
        self.assertEqual(result, "RHEINMETALL AG")

        result = analysis.lookup_stock_abr_in_all_names("Beiersdorf")
        self.assertEqual(result, "BEIERSDORF AG O.N.")

        result = analysis.lookup_stock_abr_in_all_names("Adidas")
        self.assertEqual(result, "ADIDAS AG NA O.N.")

        self.assertRaises(AttributeError, analysis.lookup_stock_abr_in_all_names, "XCERET")
