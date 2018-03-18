import unittest
from datetime import datetime
from Utils.file_utils import read_tickers_from_file
from newsFeedReader.traderfox_hp_news import read_news_from_traderfox, is_date_actual
from newsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews

test_filepath = 'C:\\temp\\test_data\\'
test_url = "https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-2-5-8-12/"


class NewsReaderTests(unittest.TestCase):
    def test_read_from_traderfox(self):
        # TODO hash temp disabled, if performance good enough without hash
        # test_file = test_filepath + "news_hashes.txt"
        test_file = "C:\\temp\\last_date_time.csv"

        with open(test_file, "w") as myfile:
            myfile.write("last_check_date" + "\n")
            myfile.write("08.03.2018 um 02:17" + "\n")

        # write new hash to reload
        # last_id = get_hash_from_file(test_file, test_url)
        # replace_in_file(test_file, last_id, "123")  # replace --> read
        news = read_news_from_traderfox(test_file)
        self.assertGreater(len(news), 0)

        # should not read again
        news = read_news_from_traderfox(test_file)
        self.assertEqual(0, len(news))  # no news should be read

    def test_read_from_traderfox_performance(self):
        # TODO hash temp disabled, if performance good enough without hash
        # test_file = test_filepath + "news_hashes.txt"
        # write new hash to reload
        # last_id = get_hash_from_file(test_file, test_url)
        # replace_in_file(test_file, last_id, "123")  # replace --> read

        test_file = "C:\\temp\\last_date_time.csv"

        with open(test_file, "w") as myfile:
            myfile.write("last_check_date" + "\n")
            myfile.write("08.03.2018 um 02:17" + "\n")

        thr_start = datetime.now()
        news = read_news_from_traderfox(test_file)

        txt = "\n\nRuntime test_read_from_traderfox_performance: " + str(datetime.now() - thr_start)
        print(txt)
        self.assertGreater(len(news), 0)

    def test_analyse_single_news(self):
        filepath = 'C:\\temp\\'
        tickers_file_name = "stock_tickers.pickle"
        stocknames_file_name = "stock_names.pickle"
        tickers_file = filepath + tickers_file_name
        stocknames_file = filepath + stocknames_file_name
        res = read_tickers_from_file(tickers_file, stocknames_file)
        ##########################

        thr_start = datetime.now()
        analysis = GermanTaggerAnalyseNews(res['names'], res['tickers'])

        news = "ANALYSE-FLASH: Credit Suisse nimmt Apple mit 'Underperform' wieder auf"
        result = analysis.analyse_single_news(news)
        t1 = round(result['prob_dist'].prob("neg"), 2)
        self.assertEqual(result['name'], "Apple Inc.")
        self.assertGreater(t1, 0.7)

        news = "ANALYSE-FLASH: Independent Research senkt Ziel für Apple auf 118 Euro"
        result = analysis.analyse_single_news(news)
        t1 = round(result['prob_dist'].prob("neg"), 2)
        self.assertEqual(result['name'], "Apple Inc.")
        self.assertGreater(t1, 0.7)

        news = "05.03.2018, ANALYSE-FLASH: NordLB hebt Apple auf 'Kaufen' - Ziel 125 Euro"
        result = analysis.analyse_single_news(news)
        t1 = round(result['prob_dist'].prob("pos"), 2)
        self.assertGreater(t1, 0.7)

        # CDAX companies

        news = "ANALYSE-FLASH: Credit Suisse nimmt Adidas mit 'Underperform' wieder auf"
        result = analysis.analyse_single_news(news)
        t1 = round(result['prob_dist'].prob("neg"), 2)
        self.assertGreater(t1, 0.7)
        self.assertEqual(result['name'], "ADIDAS AG NA O.N.")
        self.assertEqual(result['ticker'], "ADS")

        news = "ANALYSE-FLASH: Independent Research senkt Ziel für Beiersdorf auf 118 Euro"
        result = analysis.analyse_single_news(news)
        t1 = round(result['prob_dist'].prob("neg"), 2)
        self.assertGreater(t1, 0.7)
        self.assertEqual(result['name'], "BEIERSDORF AG O.N.")
        self.assertEqual(result['ticker'], "BEI")

        news = "05.03.2018, ANALYSE-FLASH: NordLB hebt Rheinmetall auf 'Kaufen' - Ziel 125 Euro"
        result = analysis.analyse_single_news(news)
        t1 = round(result['prob_dist'].prob("pos"), 2)
        self.assertGreater(t1, 0.7)
        result = analysis.lookup_stock_abr_in_all_names("Rheinmetall")
        self.assertEqual(result, "RHEINMETALL AG")

        news ="DZ Bank empfiehlt Sixt-Aktie nach starken Geschäftszahlen zum Kauf"
        result = analysis.analyse_single_news(news)
        t1 = round(result['prob_dist'].prob("pos"), 2)
        self.assertGreater(t1, 0.7)

        txt = "\n\nRuntime : " + str(datetime.now() - thr_start)
        print(txt)

    def test_lookup_stock_abr_in_all_names(self):
        filepath = 'C:\\temp\\'
        tickers_file_name = "stock_tickers.pickle"
        stocknames_file_name = "stock_names.pickle"
        tickers_file = filepath + tickers_file_name
        stocknames_file = filepath + stocknames_file_name
        res = read_tickers_from_file(tickers_file, stocknames_file)
        ##########################

        analysis = GermanTaggerAnalyseNews(res['names'], res['tickers'])

        result = analysis.lookup_stock_abr_in_all_names("Rheinmetall")
        self.assertEqual(result, "RHEINMETALL AG")

        result = analysis.lookup_stock_abr_in_all_names("Beiersdorf")
        self.assertEqual(result, "BEIERSDORF AG O.N.")

        result = analysis.lookup_stock_abr_in_all_names("Adidas")
        self.assertEqual(result, "ADIDAS AG NA O.N.")

        result = analysis.lookup_stock_abr_in_all_names("XCERET")
        self.assertEqual(result, " ")

    def test_date_check(self):

        last_date_time_str = "07.03.2018 um 03:11"
        date_time = "07.03.2018 um 23:11"

        test_file = "C:\\temp\\test_data\\last_date_time.csv"
        with open(test_file, "w") as myfile:
            myfile.write("last_check_date" + "\n")
            myfile.write(last_date_time_str + "\n")

        datetime_object = datetime.strptime(date_time, "%d.%m.%Y um %H:%M")
        is_actual, date_time = is_date_actual(datetime_object, test_file)
        self.assertEqual(is_actual, True)

        # 2. try with same date time --> not new --> false
        is_actual, date_time = is_date_actual(datetime_object, test_file)
        self.assertEqual(is_actual, False)

    def test_read_tickers_from_file(self):

        filepath = 'C:\\temp\\'
        tickers_file_name = "stock_tickers.pickle"
        stocknames_file_name = "stock_names.pickle"
        tickers_file = filepath + tickers_file_name
        stocknames_file = filepath + stocknames_file_name
        res = read_tickers_from_file(tickers_file, stocknames_file)

        # TODO self.assertEqual(len(res['tickers']), 505)
        self.assertEqual(len(res['tickers']), 818)

    def test_analyse_all_news(self):
        num_of_news_per_thread = 1
        all_news = []
        news_elringklinger = "ANALYSE-FLASH: JPMorgan belässt ElringKlinger nach Zahlen auf 'Underweight'"
        news_freenet = "ANALYSE-FLASH: DZ Bank senkt Freenet auf 'Halten' und fairen Wert auf 28 Euro"
        all_news.append(news_elringklinger)
        all_news.append(news_freenet)
        text_analysis = GermanTaggerAnalyseNews()
        result = text_analysis.analyse_all_news(all_news, num_of_news_per_thread)

        # TODO umbauen auf: https://stackoverflow.com/questions/4391697/find-the-index-of-a-dict-within-a-list-by-matching-the-dicts-value
        freenet_idx = next((index for (index, d) in enumerate(result) if d["orig_news"] == news_freenet), None)
        elringklinger_idx = next(
            (index for (index, d) in enumerate(result) if d["orig_news"] == news_elringklinger), None)

        t1 = round(result[freenet_idx]['prob_dist'].prob("neg"), 2)
        self.assertGreater(t1, 0.7)
        self.assertEqual(result[freenet_idx]['name'], "FREENET AG NA")

        t2 = round(result[elringklinger_idx]['prob_dist'].prob("neg"), 2)
        self.assertGreater(t2, 0.7)
        self.assertEqual(result[elringklinger_idx]['name'], "ELRINGKLINGER AG NA O.N.")


    def test_identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(self):
        filepath = 'C:\\temp\\'
        tickers_file_name = "stock_tickers.pickle"
        stocknames_file_name = "stock_names.pickle"
        tickers_file = filepath + tickers_file_name
        stocknames_file = filepath + stocknames_file_name
        res = read_tickers_from_file(tickers_file, stocknames_file)
        ##########################
        analysis = GermanTaggerAnalyseNews(res['names'], res['tickers'])

        news = "ANALYSE-FLASH: Credit Suisse nimmt Rheinmetall mit 'Underperform' wieder auf"
        result = analysis.identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news)
        self.assertEqual(result['name'], "RHEINMETALL AG")
        self.assertEqual(result['ticker'], "RHM")
        self.assertEqual(result['price'], 0)

        news = "ANALYSE-FLASH: Independent Research senkt Ziel für Beiersdorf auf 118 Euro"
        result = analysis.identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news)
        self.assertEqual(result['name'], "BEIERSDORF AG O.N.")
        self.assertEqual(result['ticker'], "BEI")
        self.assertEqual(result['price'], "118")

        news = "ANALYSE-FLASH: Credit Suisse nimmt Adidas mit 'Underperform' wieder auf"
        result = analysis.identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news)
        self.assertEqual(result['name'], "ADIDAS AG NA O.N.")
        self.assertEqual(result['ticker'], "ADS")

        news = "ANALYSE-FLASH: NordLB hebt Apple auf 'Kaufen' - Ziel 125 Dollar"
        result = analysis.identify_stock_and_price_from_news_nltk_german_classifier_data_nouns(news)
        self.assertEqual(result['name'], "Apple Inc.")
        self.assertEqual(result['ticker'], "AAPL")
        self.assertEqual(result['price'], "125")

