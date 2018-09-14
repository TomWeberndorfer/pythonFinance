import unittest

import backtrader as bt
import backtrader.analyzers as btanalyzer
import pandas as pd
import datetime

from backtrader.feeds import GenericCSVData

from Backtesting.Backtrader.BacktraderWrapper import BacktraderWrapper
# from directory UnitTests to --> root folder with: ..\\..\\
from Utils.CommonUtils import is_next_day_or_later
from Utils.FileUtils import is_date_actual
from Utils.GlobalVariables import *
import unittest

import backtrader as bt
import backtrader.analyzers as btanalyzer
import pandas as pd
from datetime import datetime
from time import sleep
from backtrader.feeds import GenericCSVData

from AutomaticTrading.IBPyInteractiveBrokers import IBPyInteractiveBrokers
from Backtesting.Backtrader.BacktraderWrapper import BacktraderWrapper
# from directory UnitTests to --> root folder with: ..\\..\\
from Utils.GlobalVariables import *


class TestIbPyInteractiveBrokers(unittest.TestCase):

    def test_backtrader_execute_order__no_error_message(self):
        orders_test_file = GlobalVariables.get_test_data_files_path() + "orders_test.csv"
        broker = IBPyInteractiveBrokers(orders_test_file)
        # Create a contract in GOOG stock via SMART order routing
        ######
        stock_ticker = 'GOOG'
        action = 'BUY'
        order_type = 'LMT'  # 'MKT'
        limit_price = 1000.0
        qty = 5

        broker.connect()
        broker.execute_order(stock_ticker, order_type, action, qty,
                             limit_price)
        sleep(0.5)
        error_message_list = broker.get_and_clear_error_message_list()
        broker.disconnect()

        self.assertEqual(0, len(error_message_list))

    def test__save_current_order__and__read_current_order_id__read_last__write_last_plus_1__read_again(self):
        orders_test_file = GlobalVariables.get_test_data_files_path() + "orders_test.csv"
        broker = IBPyInteractiveBrokers(orders_test_file)

        curr_order_id = broker._read_current_order_id()
        broker._save_current_order(curr_order_id, "TestTicker")
        next_order_id = broker._read_current_order_id()
        self.assertEqual(curr_order_id + 1, next_order_id)

    def test__save_current_order__read_orders__compare_date_not_later(self):
        orders_test_file = GlobalVariables.get_test_data_files_path() + "orders_test.csv"
        broker = IBPyInteractiveBrokers(orders_test_file)

        curr_order_id = broker._read_current_order_id()
        broker._save_current_order(curr_order_id, "TestTicker_2")

        orders = broker.read_orders()
        date_time_str = ""

        for curr_order_num in range(len(orders)):
            if orders['stock_ticker'][curr_order_num].startswith("TestTicker_2"):
                date_time_str = (orders['datetime'][curr_order_num])  # the last one

        is_later = is_next_day_or_later(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f", date_time_str,
                                        "%Y-%m-%d %H:%M:%S.%f")
        # written and read one are equal
        self.assertEqual(is_later, False)
        self.assertGreater(len(orders), 0)

    def test_all(self):
        orders_test_file = GlobalVariables.get_test_data_files_path() + "orders_test.csv"
        broker = IBPyInteractiveBrokers(orders_test_file)
        date_time_str = ""
        curr_order_id = broker._read_current_order_id()
        broker._save_current_order(curr_order_id, "TestTicker_2")

        orders = broker.read_orders()

        for curr_order_num in range(len(orders)):
            if orders['stock_ticker'][curr_order_num].startswith("TestTicker_2"):
                date_time_str = (orders['datetime'][curr_order_num])  # the last one

        is_later = is_next_day_or_later(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f", date_time_str,
                                        "%Y-%m-%d %H:%M:%S.%f")
        # written and read one are equal
        self.assertEqual(is_later, False)
        self.assertGreater(len(orders), 0)
