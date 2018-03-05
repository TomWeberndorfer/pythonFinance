import unittest
import pandas as pd

from Utils.file_utils import replace_in_file, get_hash_from_file
from newsFeedReader.traderfox_hp_news import read_news_from_traderfox

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
