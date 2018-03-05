import unittest
import datetime
from Utils.file_utils import replace_in_file, get_hash_from_file, read_tickers_from_file
from newsFeedReader.traderfox_hp_news import read_news_from_traderfox
from newsTrading.TextBlobAnalyseNews import TextBlobAnalyseNews

test_filepath = 'C:\\temp\\test_data\\'
test_url = "https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-2-5-8-12/"


class NewsReaderTests(unittest.TestCase):
    def test_read_from_traderfox(self):
        test_file = test_filepath + "news_hashes.txt"

        # write new hash to reload
        last_id = get_hash_from_file(test_file, test_url)
        replace_in_file(test_file, last_id, "123")  # replace --> read
        news = read_news_from_traderfox(test_file)
        self.assertGreater(len(news), 0)

        # should not read again
        news = read_news_from_traderfox(test_file)
        self.assertEqual(0, len(news))  # no news should be read

    def test_analyse(self):
        filepath = 'C:\\temp\\'
        tickers_file_name = "stock_tickers.pickle"
        stocknames_file_name = "stock_names.pickle"
        tickers_file = filepath + tickers_file_name
        stocknames_file = filepath + stocknames_file_name
        res = read_tickers_from_file(tickers_file, stocknames_file)
        ##########################

        thr_start = datetime.datetime.now()
        analysis = TextBlobAnalyseNews(res['names'], res['tickers'])

        news = "ANALYSE-FLASH: Credit Suisse nimmt Apple mit 'Underperform' wieder auf"
        r1 = analysis.analyse_single_news(news)
        t1 = round(r1['prob_dist'].prob("neg"), 2)
        self.assertEqual(t1, 0.77)

        news = "ANALYSE-FLASH: Independent Research senkt Ziel für Apple auf 118 Euro"
        r1 = analysis.analyse_single_news(news)
        t1 = round(r1['prob_dist'].prob("neg"), 2)
        self.assertEqual(t1, 0.77)

        news = "05.03.2018, ANALYSE-FLASH: NordLB hebt Apple auf 'Kaufen' - Ziel 125 Euro"
        r1 = analysis.analyse_single_news(news)
        t1 = round(r1['prob_dist'].prob("pos"), 2)
        self.assertEqual(t1, 0.77)

        # CDAX companies

        news = "ANALYSE-FLASH: Credit Suisse nimmt Adidas mit 'Underperform' wieder auf"
        r1 = analysis.analyse_single_news(news)
        t1 = round(r1['prob_dist'].prob("neg"), 2)
        self.assertEqual(t1, 0.77)

        news = "ANALYSE-FLASH: Independent Research senkt Ziel für Beiersdorf auf 118 Euro"
        # TODO: statt für nimmt er beiersdorf --> english umwandeln funzt da a ned
        r1 = analysis.analyse_single_news(news)
        t1 = round(r1['prob_dist'].prob("neg"), 2)
        self.assertEqual(t1, 0.77)

        news = "05.03.2018, ANALYSE-FLASH: NordLB hebt Rheinmetall auf 'Kaufen' - Ziel 125 Euro"
        r1 = analysis.analyse_single_news(news)
        t1 = round(r1['prob_dist'].prob("pos"), 2)
        self.assertEqual(t1, 0.77)

        txt = "\n\nRuntime : " + str(datetime.datetime.now() - thr_start)
        print(txt)

    def test_identify_stock(self):
        filepath = 'C:\\temp\\'
        tickers_file_name = "stock_tickers.pickle"
        stocknames_file_name = "stock_names.pickle"
        tickers_file = filepath + tickers_file_name
        stocknames_file = filepath + stocknames_file_name
        res = read_tickers_from_file(tickers_file, stocknames_file)
        ##########################

        analysis = TextBlobAnalyseNews(res['names'], res['tickers'])

        news = "ANALYSE-FLASH: Credit Suisse nimmt Rheinmetall mit 'Underperform' wieder auf"
        result = analysis.identify_stock_in_news(news)
        self.assertEqual(result['name'], "RHEINMETALL AG")
        self.assertEqual(result['ticker'], "RHM")

        news = "ANALYSE-FLASH: Independent Research senkt Ziel für Beiersdorf auf 118 Euro"
        result = analysis.identify_stock_in_news(news)
        self.assertEqual(result['name'], "BEIERSDORF AG O.N.")
        self.assertEqual(result['ticker'], "BEI")

        news = "ANALYSE-FLASH: Credit Suisse nimmt Adidas mit 'Underperform' wieder auf"
        result = analysis.identify_stock_in_news(news)
        self.assertEqual(result['name'], "ADIDAS AG NA O.N.")
        self.assertEqual(result['ticker'], "ADS")

    def test_lookup_stock_abr_in_all_names(self):
        filepath = 'C:\\temp\\'
        tickers_file_name = "stock_tickers.pickle"
        stocknames_file_name = "stock_names.pickle"
        tickers_file = filepath + tickers_file_name
        stocknames_file = filepath + stocknames_file_name
        res = read_tickers_from_file(tickers_file, stocknames_file)
        ##########################

        analysis = TextBlobAnalyseNews(res['names'], res['tickers'])

        result = analysis.lookup_stock_abr_in_all_names("Rheinmetall")
        self.assertEqual(result, "RHEINMETALL AG")

        result = analysis.lookup_stock_abr_in_all_names("Beiersdorf")
        self.assertEqual(result, "BEIERSDORF AG O.N.")

        result = analysis.lookup_stock_abr_in_all_names("Adidas")
        self.assertEqual(result, "ADIDAS AG NA O.N.")

        #TODO fails einbauen, damit man sieht das ned alles geht
