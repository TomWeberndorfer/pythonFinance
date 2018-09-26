from datetime import datetime
from pathlib import Path
from unittest import TestCase
from apscheduler.schedulers.background import BackgroundScheduler

from AutomaticTrading.InteractiveBrokers.IBPyInteractiveBrokers import IBPyInteractiveBrokers
from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Utils.CommonUtils import CommonUtils, is_next_day_or_later
from Utils.FileUtils import FileUtils
from Utils.GlobalVariables import *
from time import sleep

from Utils.StockDataUtils import buy_recommendations


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
        # TODO testen der konvertierung mittels strptime "um"
        # date_time = "14.03.2018 um 23:11"
        # datetime_object = datetime.strptime(date_time, "%d.%m.%Y um %H:%M")
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

    def test_get_implemented_items_dict(self):
        path = Path(os.path.dirname(os.path.abspath(__file__)))
        test_dict = CommonUtils.get_implemented_items_dict(path, './*/**/**/*.py', "TestClassForUtils")
        self.assertEqual(1, len(test_dict))
        self.assertEqual("TestClassForUtils", list(test_dict.keys())[0])

    def test_is_date_current(self):
        last_date_time_str = "07.03.2018 um 03:11"
        date_time_str = "2018-09-13 18:16:21.563728"

        is_actual = is_next_day_or_later(date_time_str, "%Y-%m-%d %H:%M:%S.%f", last_date_time_str, "%d.%m.%Y um %H:%M")
        self.assertEqual(is_actual, True)

        date_time_str = "07.03.2018 um 03:11"
        last_date_time_str = "2018-06-13 18:16:21.563728"

        is_actual = is_next_day_or_later(date_time_str, "%d.%m.%Y um %H:%M", last_date_time_str, "%Y-%m-%d %H:%M:%S.%f")
        self.assertEqual(is_actual, False)

    def test_background_scheduler_interval__increase_every_0s1(self):
        background_scheduler = BackgroundScheduler()
        bt = background_test_dummy()
        background_scheduler.add_job(bt.set, 'interval', seconds=0.1)
        background_scheduler.start()
        sleep(0.15)
        self.assertEqual(1, bt.get())
        sleep(0.06)
        self.assertEqual(2, bt.get())
        background_scheduler.shutdown()
        sleep(0.1)
        self.assertEqual(2, bt.get())

    def test_buy_recommendations__apple_today__not_buy(self):
        orders_test_file = GlobalVariables.get_test_data_files_path() + "orders_test.csv"
        broker = IBPyInteractiveBrokers(orders_test_file)

        # insert apple as last entry today
        curr_order_id = broker._read_current_order_id()
        broker._save_current_order(curr_order_id, "AAPL")

        container = StockDataContainer("Apple Inc.", "AAPL", "en")
        container.set_stop_buy(12)
        container.set_stop_loss(10)
        container.set_position_size(200)
        container.update_used_strategy_and_recommendation("TestStrategy", "BUY")

        stocks = [container]
        max_num_of_different_stocks_to_buy = 2

        buy_recommendations(broker, stocks, max_num_of_different_stocks_to_buy)
        sleep(0.5)
        error_message_list = broker.get_and_clear_error_message_list()

        # the order id should be the next to the last manual entry,
        # because nothing should be bought
        next_order_id = broker._read_current_order_id()
        self.assertEqual(curr_order_id + 1, next_order_id)
        self.assertEqual(0, len(error_message_list))


class background_test_dummy:
    """
    Test dummy for background running test
    """
    def __init__(self):
        self.var = 0

    def set(self):
        self.var = self.var + 1

    def get(self):
        return self.var
