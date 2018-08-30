import unittest
from datetime import datetime

from DataReading.DataReaderFactory import DataReaderFactory

from Utils.file_utils import read_tickers_from_file_or_web
from newsFeedReader.traderfox_hp_news import is_date_actual
from Utils.GlobalVariables import *

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\TestData\\'


class TestNewsReader(unittest.TestCase):

    def test_sample(self):
        # TODO
        # ++++++++++ FOR SAMPLE NEWS
        # data = pd.read_csv(GlobalVariables.get_data_files_path() + "Sample_news.txt")
        data = []
        # all_news = data.News.tolist()

        # all_news.append("ANALYSE-FLASH: NordLB senkt Apple auf 'Kaufen' - Ziel 125,5 Euro")
        # all_news.append("Bryan Garnier hebt Apple auf 'Buy' - Ziel 91 Euro")

    def test_read_from_traderfox(self):
        # TODO ois mit file is kein unit test
        test_file = filepath + "\\last_date_time.csv"

        with open(test_file, "w") as myfile:
            myfile.write("last_check_date" + "\n")
            myfile.write("01.01.2018 um 02:17" + "\n")

        stock_data_container_list = []
        data_storage = DataReaderFactory()
        reader_type = 'TraderfoxNewsDataReader'
        data_reader_params = {'Name': 'TraderfoxNewsDataReader', 'last_date_time_file': test_file,
                              'german_tagger': 'C:\\temp\\pythonFinance\\pythonFinance\\DataFiles\\nltk_german_classifier_data.pickle',
                              'reload_data': True, 'ticker_needed': False}

        reader = data_storage.prepare(reader_type, stock_data_container_list,
                                      False,
                                      data_reader_params)
        reader.read_data()
        self.assertGreater(len(stock_data_container_list), 0)

        # should not read again
        stock_data_container_list = []
        reader.read_data()
        self.assertEqual(len(stock_data_container_list), 0)

    def test_date_check(self):
        last_date_time_str = "07.03.2018 um 03:11"
        date_time = "07.03.2018 um 23:11"

        test_file = filepath + "\\last_date_time.csv"
        with open(test_file, "w") as myfile:
            myfile.write("last_check_date" + "\n")
            myfile.write(last_date_time_str + "\n")

        datetime_object = datetime.strptime(date_time, "%d.%m.%Y um %H:%M")
        is_actual, date_time = is_date_actual(datetime_object, test_file)
        self.assertEqual(is_actual, True)

        # 2. try with same date time --> not new --> false
        is_actual, date_time = is_date_actual(datetime_object, test_file)
        self.assertEqual(is_actual, False)

    def test_read_tickers_from_file_or_web(self):
        stock_data_container_file_name = "stock_data_container_file.pickle"
        stock_data_container_file = filepath + stock_data_container_file_name

        # TODO 11: seite geht nicht mehr
        list_with_stock_pages_to_read = [
            ['http://en.wikipedia.org/wiki/List_of_S%26P_500_companies', 'table', 'class',
             'wikitable sortable', 0, 1, 'en'],
            ['http://topforeignstocks.com/stock-lists/the-list-of-listed-companies-in-germany/',
             'tbody', 'class', 'row-hover', 2, 1, 'de']]

        stock_data_container_list = read_tickers_from_file_or_web(stock_data_container_file, True,
                                                                  list_with_stock_pages_to_read)
        self.assertGreater(len(stock_data_container_list), 800)

        stock_data_container_list = read_tickers_from_file_or_web(stock_data_container_file, False,
                                                                  list_with_stock_pages_to_read)
        self.assertGreater(len(stock_data_container_list), 800)
