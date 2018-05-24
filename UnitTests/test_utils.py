from unittest import TestCase
import pandas as pd
from datetime import datetime

from Utils.common_utils import send_email, is_date_today
from Utils.file_utils import check_file_exists_or_create


class TestUtils(TestCase):
    def test_calc_avg_vol(self):
        self.assertEqual(1,1) #TODO????


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

    def test_is_date_today(self):
        date_time = "07.03.2018 um 23:11"
        datetime_object = datetime.strptime(date_time, "%d.%m.%Y um %H:%M")
        self.assertEqual(is_date_today(datetime_object), False)

        date_time = "14.03.2018 um 23:11" #TODO
        datetime_object = datetime.strptime(date_time, "%d.%m.%Y um %H:%M")
        self.assertEqual(is_date_today(datetime_object), True)