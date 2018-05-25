import unittest
from datetime import datetime

import os

from DataReading.StockDataContainer import StockDataContainer
from Utils.file_utils import FileUtils, read_tickers_from_file
from newsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews

# from directory UnitTests to --> root folder with: ..\\..\\
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestGermanTaggerAnalyseNews(unittest.TestCase):

    def test_analyse_single_news(self):
        stock_data_container_list = [StockDataContainer("RWE AG ST O.N.", "RWE", "de"),
                                     StockDataContainer("RHEINMETALL AG", "RHM", "de"),
                                     StockDataContainer("BEIERSDORF AG O.N.", "BEI", "de"),
                                     StockDataContainer("ADIDAS AG NA O.N.", "ADS", "de"),
                                     StockDataContainer("Apple Inc.", "AAPL", "en"),
                                     StockDataContainer("BET-AT-HOME.COM AG O.N.", "ACX", "de"),
                                     StockDataContainer("Roche Holding AG", "RHHBY", ""),
                                     StockDataContainer("LOrealfuture", "LORFK8.EX", "")]

        thr_start = datetime.now()
        analysis = GermanTaggerAnalyseNews(stock_data_container_list, 0.7,
                                           filepath + 'nltk_german_classifier_data.pickle')

        news = "ANALYSE-FLASH: Credit Suisse nimmt RWE mit 'Outperform' wieder auf"
        result = analysis.analyse_single_news(news)
        t1 = round(result.prob_dist.prob("pos"), 2)
        self.assertEqual(result.stock_name, "RWE AG ST O.N.")
        self.assertGreater(t1, 0.7)

        news = "19.03.2018 um 08:58, ANALYSE-FLASH: HSBC senkt RWE auf 'Reduce' - Ziel 18 Euro"
        result = analysis.analyse_single_news(news)
        t1 = round(result.prob_dist.prob("neg"), 2)
        self.assertEqual(result.stock_name, "RWE AG ST O.N.")
        self.assertGreater(t1, 0.7)

        news = "ANALYSE-FLASH: Credit Suisse nimmt Apple mit 'Underperform' wieder auf"
        result = analysis.analyse_single_news(news)
        t1 = round(result.prob_dist.prob("neg"), 2)
        self.assertEqual(result.stock_name, "Apple Inc.")
        self.assertGreater(t1, 0.7)

        news = "ANALYSE-FLASH: Independent Research senkt Ziel für Apple auf 118 Euro"
        result = analysis.analyse_single_news(news)
        t1 = round(result.prob_dist.prob("neg"), 2)
        self.assertEqual(result.stock_name, "Apple Inc.")
        self.assertGreater(t1, 0.7)

        news = "05.03.2018, ANALYSE-FLASH: NordLB hebt Apple auf 'Kaufen' - Ziel 125 Euro"
        result = analysis.analyse_single_news(news)
        t1 = round(result.prob_dist.prob("pos"), 2)
        self.assertGreater(t1, 0.7)

        # CDAX companies
        news = "ANALYSE-FLASH: Credit Suisse nimmt Adidas mit 'Underperform' wieder auf"
        result = analysis.analyse_single_news(news)
        t1 = round(result.prob_dist.prob("neg"), 2)
        self.assertGreater(t1, 0.7)
        self.assertEqual(result.stock_name, "ADIDAS AG NA O.N.")
        self.assertEqual(result.stock_ticker, "ADS")

        news = "ANALYSE-FLASH: Independent Research senkt Ziel für Beiersdorf auf 118 Euro"
        result = analysis.analyse_single_news(news)
        t1 = round(result.prob_dist.prob("neg"), 2)
        self.assertGreater(t1, 0.7)
        self.assertEqual(result.stock_name, "BEIERSDORF AG O.N.")
        self.assertEqual(result.stock_ticker, "BEI")

        news = "05.03.2018, ANALYSE-FLASH: NordLB hebt Rheinmetall auf 'Kaufen' - Ziel 125 Euro"
        result = analysis.analyse_single_news(news)
        t1 = round(result.prob_dist.prob("pos"), 2)
        self.assertGreater(t1, 0.7)
        self.assertEqual(result.stock_name, "RHEINMETALL AG")

        news = "DZ Bank empfiehlt Sixt-Aktie nach starken Geschäftszahlen zum Kauf"
        result = analysis.analyse_single_news(news)
        t1 = round(result.prob_dist.prob("pos"), 2)
        self.assertGreater(t1, 0.7)

        # should fail and return " "
        news = "01.03.2018, Das sagen Ökonomen zur bevorstehenden Wahl in Italien"
        result = analysis.analyse_single_news(news)
        self.assertEqual("", result.stock_name)

        news = "17.03.2018 um 09:05, PROSIEBENSAT.1 IM FOKUS: Dax-Absteiger stellt Weichen für bessere Zeiten"
        result = analysis.analyse_single_news(news)
        self.assertEqual("", result.stock_name)

        txt = "\n\nRuntime : " + str(datetime.now() - thr_start)
        print(txt)

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
                                           filepath + 'nltk_german_classifier_data.pickle')

        news = "ANALYSE-FLASH: Jefferies hebt Ziel für RWE auf 250 US-Dollar - 'Underperform'"
        result = analysis._identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news)
        self.assertEqual(result.stock_name, "RWE AG ST O.N.")
        self.assertEqual(result.stock_ticker, "RWE")
        self.assertEqual(result.stock_exchange, "de")
        self.assertEqual(result.stock_target_price, 250)

        # no price --> 0
        news = "19.03.2018 um 08:21, ANALYSE-FLASH: Credit Suisse nimmt RWE mit 'Outperform' wieder auf"
        result = analysis._identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news)
        self.assertEqual(result.stock_name, "RWE AG ST O.N.")
        self.assertEqual(result.stock_ticker, "RWE")
        self.assertEqual(result.stock_exchange, "de")
        self.assertEqual(result.stock_target_price, 0)

        news = "ANALYSE-FLASH: Credit Suisse nimmt Rheinmetall mit 'Underperform' wieder auf"
        result = analysis._identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news)
        self.assertEqual(result.stock_name, "RHEINMETALL AG")
        self.assertEqual(result.stock_ticker, "RHM")
        self.assertEqual(result.stock_exchange, "de")
        self.assertEqual(result.stock_target_price, 0)

        # price with german coma, should also be possible
        news = "ANALYSE-FLASH: Independent Research senkt Ziel für Beiersdorf auf 118,7 Euro"
        result = analysis._identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news)
        self.assertEqual(result.stock_name, "BEIERSDORF AG O.N.")
        self.assertEqual(result.stock_ticker, "BEI")
        self.assertEqual(result.stock_exchange, "de")
        self.assertEqual(result.stock_target_price, 118.7)

        # price with english comma
        news = "ANALYSE-FLASH: Independent Research senkt Ziel für Beiersdorf auf 118.7 Euro"
        result = analysis._identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news)
        self.assertEqual(result.stock_name, "BEIERSDORF AG O.N.")
        self.assertEqual(result.stock_ticker, "BEI")
        self.assertEqual(result.stock_exchange, "de")
        self.assertEqual(result.stock_target_price, 118.7)

        news = "ANALYSE-FLASH: Credit Suisse nimmt Adidas mit 'Underperform' wieder auf"
        result = analysis._identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news)
        self.assertEqual(result.stock_name, "ADIDAS AG NA O.N.")
        self.assertEqual(result.stock_exchange, "de")
        self.assertEqual(result.stock_ticker, "ADS")

        news = "ANALYSE-FLASH: NordLB hebt Apple auf 'Kaufen' - Ziel 125 Dollar"
        result = analysis._identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news)
        self.assertEqual(result.stock_name, "Apple Inc.")
        self.assertEqual(result.stock_ticker, "AAPL")
        self.assertEqual(result.stock_exchange, "en")
        self.assertEqual(result.stock_target_price, 125)

        news = "Credit Suisse nimmt RWE mit 'Outperform' wieder auf"
        result = analysis._identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news)
        self.assertEqual(result.stock_name, "RWE AG ST O.N.")
        self.assertEqual(result.stock_ticker, "RWE")
        self.assertEqual(result.stock_exchange, "de")
        self.assertEqual(result.stock_target_price, 0)

        news = "ANALYSE-FLASH: Hauck & Aufhäuser senkt Bet-at-home auf 'Hold' - Ziel 89 Euro"
        result = analysis._identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news)
        self.assertEqual(result.stock_name, 'BET-AT-HOME.COM AG O.N.')
        self.assertEqual(result.stock_ticker, "ACX")
        self.assertEqual(result.stock_exchange, "de")
        self.assertEqual(result.stock_target_price, 89)

        # not in stock list --> read stock tickers and names from webservice
        news = "Goldman belässt Roche auf conviction buy list"
        result = analysis._identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news)
        self.assertEqual(result.stock_name, 'Roche Holding AG')
        self.assertEqual(result.stock_ticker, "RHHBY")
        self.assertEqual(result.stock_exchange, "")
        self.assertEqual(result.stock_target_price, 0)

        news = "Jefferies senkt Ziel für Loreal auf 186 euro Hold"
        result = analysis._identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news)
        self.assertEqual(result.stock_name, 'LOrealfuture')
        # TODO des ändeert se imma: - LORFM8.EX oder LORFK8.EX
        #  self.assertEqual(result.stock_ticker, "LORFK8.EX")
        self.assertEqual(result.stock_exchange, "")
        self.assertEqual(result.stock_target_price, 186)

    def test_analyse_all_news(self):
        stock_data_container_list = [StockDataContainer("FREENET AG NA", "", ""),
                                     StockDataContainer("ELRINGKLINGER AG NA O.N.", "", "")]

        num_of_news_per_thread = 1
        all_news = []
        news_elringklinger = "ANALYSE-FLASH: JPMorgan belässt ElringKlinger nach Zahlen auf 'Underweight'"
        news_freenet = "ANALYSE-FLASH: DZ Bank senkt Freenet auf 'Halten' und fairen Wert auf 28 Euro"
        all_news.append(news_elringklinger)
        all_news.append(news_freenet)
        text_analysis = GermanTaggerAnalyseNews(stock_data_container_list, 0.7,
                                                filepath + 'nltk_german_classifier_data.pickle')
        result = text_analysis.analyse_all_news(all_news)

        self.assertEquals(len(result), 2)

        # TODO umbauen auf: https://stackoverflow.com/questions/4391697/find-the-index-of-a-dict-within-a-list-by-matching-the-dicts-value
        freenet_idx = result.index(StockDataContainer("FREENET AG NA", "", ""))
        elringklinger_idx = result.index(StockDataContainer("ELRINGKLINGER AG NA O.N.", "", ""))

        t1 = round(result[freenet_idx].prob_dist.prob("neg"), 2)
        self.assertGreater(t1, 0.7)
        self.assertEqual(result[freenet_idx].stock_name, "FREENET AG NA")

        t2 = round(result[elringklinger_idx].prob_dist.prob("neg"), 2)
        self.assertGreater(t2, 0.7)
        self.assertEqual(result[elringklinger_idx].stock_name, "ELRINGKLINGER AG NA O.N.")
