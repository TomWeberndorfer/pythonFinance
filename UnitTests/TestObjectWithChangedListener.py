import re
from unittest import TestCase
import pandas as pd
from datetime import datetime

from Utils.ListWithChangedListeners import ListWithChangedListeners, DictWithChangedListeners, \
    ObjectWithChangedListeners
from Utils.common_utils import send_email, is_date_today
from Utils.file_utils import check_file_exists_or_create, FileUtils
from Utils.GlobalVariables import *


class ListenerClass:
    def __init__(self):
        self.temp_value = 0

    def temp_listener_method(self):
        self.temp_value = self.temp_value + 1

    def get_temp_value(self):
        return self.temp_value

    def reset_temp_value(self):
        self.__init__()


class TestObjectWithChangedListener(TestCase):

    def test_ListWithChangedListeners__init__add_listener__append__get__clear(self):
        my_list = ListWithChangedListeners()
        listener_class = ListenerClass()
        my_list.add_event_listeners(listener_class.temp_listener_method)
        my_list.append("test")
        self.assertEqual(["test"], my_list.get())
        self.assertEqual(1, listener_class.get_temp_value())

        my_list.append("test2")
        self.assertEqual(["test", "test2"], my_list.get())
        self.assertEqual(2, listener_class.get_temp_value())

        # clear
        my_list.clear()
        self.assertEqual([], my_list.get())
        self.assertEqual(3, listener_class.get_temp_value())

    def test_DictWithChangedListeners__init__add_listener__append__get__clear(self):
        my_dict = DictWithChangedListeners()
        listener_class = ListenerClass()
        my_dict.add_event_listeners(listener_class.temp_listener_method)
        my_dict.update({"key1": "value1"})
        self.assertEqual({"key1": "value1"}, my_dict.get())
        self.assertEqual(1, listener_class.get_temp_value())

        my_dict.update({"key2": "value2"})
        self.assertEqual({"key1": "value1", "key2": "value2"}, my_dict.get())
        self.assertEqual(2, listener_class.get_temp_value())

        # clear
        my_dict.clear()
        self.assertEqual({}, my_dict.get())
        self.assertEqual(3, listener_class.get_temp_value())

    def test_ObjectWithChangedListeners__init__add_listener__set__get__clear(self):
        my_string = ObjectWithChangedListeners()
        listener_class = ListenerClass()
        my_string.add_event_listeners(listener_class.temp_listener_method)
        my_string.set("value1")
        self.assertEqual("value1", my_string.get())
        self.assertEqual(1, listener_class.get_temp_value())

        my_string.set("value2")
        self.assertEqual("value2", my_string.get())
        self.assertEqual(2, listener_class.get_temp_value())

        # clear
        my_string.clear()
        self.assertEqual("", my_string.get())
        self.assertEqual(3, listener_class.get_temp_value())
