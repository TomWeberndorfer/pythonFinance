import re
from unittest import TestCase
import pandas as pd
from datetime import datetime

from Utils.CommonUtils import CommonUtils
from Utils.FileUtils import FileUtils
from Utils.GlobalVariables import *

class TestUtils(TestCase):

    # def test_send_email(self):
    #     result = send_email(from_addr='python.trading.framework@gmail.com',
    #               to_addr_list=['weberndorfer.thomas@gmail.com'],
    #               cc_addr_list=[],
    #               subject='Aktien',
    #               message='Test',
    #               login='python.trading.framework',
    #               password='8n6Qw8YoJe8m')
    #
    #     self.assertEqual(len(result), 0)

    def test_is_date_today__not_today__today(self):
        date_time = "07.03.2018 um 23:11"
        datetime_object = datetime.strptime(date_time, "%d.%m.%Y um %H:%M")
        self.assertEqual(CommonUtils.is_date_today(datetime_object), False)

        test = datetime.now()
        #TODO testen der konvertierung mittels strptime "um"
        #date_time = "14.03.2018 um 23:11"
        #datetime_object = datetime.strptime(date_time, "%d.%m.%Y um %H:%M")
        self.assertEqual(CommonUtils.is_date_today(test), True)

    def test_append_to_file__only_new_entries__all_entries(self):
        filename = GlobalVariables.get_data_files_path() + "TestData\\NewsForBacktesting.txt"
        text = "25.07.2018 um 08:41, ANALYSE-FLASH: Berenberg hebt Ziel für Adidas auf 207 Euro - 'Hold'"
        self.assertFalse(FileUtils.append_textline_to_file(text, filename, True))

        text = str(datetime.now()) + ", Test Eintrag"
        self.assertTrue(FileUtils.append_textline_to_file(text, filename, True))

        text = "16.07.2018 um 8:51, Test Eintrag"
        self.assertTrue(FileUtils.append_textline_to_file(text, filename, False))

    def test_append_text_list_to_file__write_and_read_again__2x_only_new_data__1x_all_data(self):
        filename = GlobalVariables.get_data_files_path() + "TestData\\ScreeningResults.csv"
        test_1 = "Test 1"
        text_list = [test_1, "Test2", "Test3"]
        self.assertFalse(FileUtils.append_text_list_to_file(text_list, filename, True))

        text_list_2 = [str(datetime.now()) + ", Test Eintrag"]
        self.assertTrue(FileUtils.append_text_list_to_file(text_list_2, filename, True))

        self.assertTrue(FileUtils.append_text_list_to_file([test_1], filename, False))

        text_to_find = text_list
        text_to_find.extend(text_list_2)

        with open(filename, 'r') as myfile:
            file_content = myfile.read()
            for text in text_to_find:
                self.assertTrue(str(text) in file_content)
