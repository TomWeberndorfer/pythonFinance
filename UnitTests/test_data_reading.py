import unittest

import os

from DataRead_Google_Yahoo import get_symbol_from_name_from_topforeignstocks
from Utils.GlobalVariables import *

test_filepath = GlobalVariables.get_data_files_path() + 'TestData\\'

class DataReaderTests(unittest.TestCase):

    def test_get_symbol_from_name_from_topforeignstocks(self):
        #TODO 1:
        name, symbol = get_symbol_from_name_from_topforeignstocks("Nestle")


        name, symbol = get_symbol_from_name_from_topforeignstocks("Roche")
        self.assertEqual(name, 'Roche Holding AG')
        self.assertEqual(symbol, "RHHBY")

        name, symbol = get_symbol_from_name_from_topforeignstocks("Tesla")
        self.assertEqual(symbol, "TSLA")
        self.assertEqual(name, 'Tesla, Inc.')



