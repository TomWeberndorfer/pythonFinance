import os
import unittest

import numpy as np
import pandas as pd

from Signals.Signals import signal_is_volume_high_enough, signal_is52_w_high, \
    signal_is_volume_raising_within_check_days, signal_is_last_volume_higher_than_avg, signal_is_a_few_higher_than_avg, \
    signal_is_volume_raising
from Utils.common_utils import calc_avg_vol, calculate_stopbuy_and_stoploss

# from directory UnitTests to --> root folder with: ..\\..\\
from Utils.GlobalVariables import *

test_filepath = GlobalVariables.get_data_files_path() + 'TestData\\'


class TestSignals(unittest.TestCase):

    def convert(self):
        file = test_filepath + 'Autodesk Inc..csv'
        data = pd.read_csv(file)
        print()
        print()

        print("labels = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']")
        print(" data = [")
        for i in range(0, len(data)):
            if i == len(data) - 1:
                print("(\'{0}\', {1}, {2}, {3}, {4}, {5})]".format(str(data[GlobalVariables.get_stock_data_labels_dict()['Date']][i]), str(data[GlobalVariables.get_stock_data_labels_dict()['Open']][i]),
                                                                   str(data[GlobalVariables.get_stock_data_labels_dict()['High']][i]), str(data[GlobalVariables.get_stock_data_labels_dict()['Low']][i]),
                                                                   str(data[GlobalVariables.get_stock_data_labels_dict()['Close']][i]), str(data[GlobalVariables.get_stock_data_labels_dict()['Volume']][i])))
            else:
                #TODO des is desselbe wie oben nur klammer anders hinten
                print("(\'{0}\', {1}, {2}, {3}, {4}, {5}),".format(str(data[GlobalVariables.get_stock_data_labels_dict()['Date']][i]), str(data[GlobalVariables.get_stock_data_labels_dict()['Open']][i]),
                                                                   str(data[GlobalVariables.get_stock_data_labels_dict()['High']][i]), str(data[GlobalVariables.get_stock_data_labels_dict()['Low']][i]),
                                                                   str(data[GlobalVariables.get_stock_data_labels_dict()['Close']][i]), str(data[GlobalVariables.get_stock_data_labels_dict()['Volume']][i])))

        print ("data = pd.DataFrame.from_records(data, columns=labels)")

    def test_signal_is_volume_high_enough__volume_to_low__volume_high_enough(self):
        # volume below 15k
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-09-13', 23.6, 23.73, 23.15, 23.26, 14000),
            ('2016-09-14', 23.33, 23.43, 22.95, 23.11, 14000),
            ('2016-09-15', 23.15, 23.77, 23.14, 23.62, 14000),
            ('2016-09-16', 23.57, 23.68, 23.38, 23.5, 14000),
            ('2016-09-19', 23.6, 23.77, 23.46, 23.51, 14000),
            ('2016-09-20', 23.73, 23.76, 23.26, 23.31, 14000)]
        df = pd.DataFrame.from_records(data, columns=labels)
        self.assertEqual(signal_is_volume_high_enough(df, min_req_vol=15000), False)

        # volume above 30k
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-09-13', 23.6, 23.73, 23.15, 23.26, 16000),
            ('2016-09-14', 23.33, 23.43, 22.95, 23.11, 16000),
            ('2016-09-15', 23.15, 23.77, 23.14, 23.62, 16000),
            ('2016-09-16', 23.57, 23.68, 23.38, 23.5, 16000),
            ('2016-09-19', 23.6, 23.77, 23.46, 23.51, 16000),
            ('2016-09-20', 23.73, 23.76, 23.26, 23.31, 16000)]
        data = pd.DataFrame.from_records(data, columns=labels)
        self.assertEqual(signal_is_volume_high_enough(data), True)

    def test_signal_is52_w_high__last_val_is_higher_than_others__last_val_not_higher(self):
        # last val 52 w Hi: data High: curVal is 100, other 90
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-03', 90, 90, 100.39, 100.5, 31000),
            ('2016-10-04', 90, 90, 100.18, 100.28, 31000),
            ('2016-10-05', 90, 90, 100.27, 100.43, 31000),
            ('2016-10-06', 90, 90, 100.29, 100.48, 31000),
            ('2016-10-07', 90, 90, 100.37, 100.48, 31000),
            ('2016-10-10', 90, 90, 100.55, 100.77, 31000),
            ('2016-10-11', 90, 90, 100.01, 100.16, 31000),
            ('2016-10-12', 90, 100, 100.11, 100.18, 31000)]

        data = pd.DataFrame.from_records(data, columns=labels)
        self.assertEqual(signal_is52_w_high(data, 0.98), True)

        # last val < 0.98 hi: High: 100, lastval = 97
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-03', 100, 100, 100.39, 100.5, 31000),
            ('2016-10-04', 100, 100, 100.18, 100.28, 31000),
            ('2016-10-05', 100, 100, 100.27, 100.43, 31000),
            ('2016-10-06', 100, 100, 100.29, 100.48, 31000),
            ('2016-10-07', 100, 100, 100.37, 100.48, 31000),
            ('2016-10-10', 100, 100, 100.55, 100.77, 31000),
            ('2016-10-11', 100, 100, 100.01, 100.16, 31000),
            ('2016-10-12', 100, 97, 100.11, 100.18, 31000)]

        data = pd.DataFrame.from_records(data, columns=labels)
        self.assertEqual(signal_is52_w_high(data, 0.98), False)

        # last val > 1.03 hi: High: 100, lastval = 104
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-03', 100, 100, 100.39, 100.5, 31000),
            ('2016-10-04', 100, 100, 100.18, 100.28, 31000),
            ('2016-10-05', 100, 100, 100.27, 100.43, 31000),
            ('2016-10-06', 100, 100, 100.29, 100.48, 31000),
            ('2016-10-07', 100, 100, 100.37, 100.48, 31000),
            ('2016-10-10', 100, 100, 100.55, 100.77, 31000),
            ('2016-10-11', 100, 100, 100.01, 100.16, 31000),
            ('2016-10-12', 101, 104, 101.0, 101.0, 32000)]

        data = pd.DataFrame.from_records(data, columns=labels)
        self.assertEqual(signal_is52_w_high(data, 0.98), True)

        # last val = 99, High is 100
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-03', 96, 96, 96.39, 96.5, 3960),
            ('2016-10-04', 96, 96, 96.18, 96.28, 3960),
            ('2016-10-05', 96, 96, 96.27, 96.43, 3960),
            ('2016-10-06', 96, 96, 96.29, 96.48, 3960),
            ('2016-10-07', 96, 96, 96.37, 96.48, 3960),
            ('2016-10-10', 96, 96, 96.55, 96.77, 3960),
            ('2016-10-11', 96, 96, 96.01, 96.16, 3960),
            ('2016-10-12', 96, 99, 101.0, 101.0, 32000)]

        data = pd.DataFrame.from_records(data, columns=labels)
        self.assertEqual(signal_is52_w_high(data, 0.98), True)

    def test_signal_is_volume_raising_within_check_days(self):
        check_days = 5
        raising_days = 3

        # t1: minimum raising
        # h,h,h,l,h
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-03', 90, 90, 100.39, 100.5, 4000),
            ('2016-10-04', 90, 90, 100.18, 100.28, 4000),
            ('2016-10-05', 90, 90, 100.27, 100.43, 4000),
            ('2016-10-06', 90, 90, 100.29, 100.48, 5000),
            ('2016-10-07', 90, 90, 100.37, 100.48, 6000),
            ('2016-10-11', 90, 90, 100.01, 100.16, 6000),
            ('2016-10-12', 90, 100, 100.11, 100.18, 11000)]

        data = pd.DataFrame.from_records(data, columns=labels)
        self.assertEqual(signal_is_volume_raising_within_check_days(data, check_days, raising_days), True)

        # h,h,l,l,h
        #file = test_filepath + 'test_isVolumeRaising_2_t1_HHLHH.csv'
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-03', 90, 90, 100.39, 100.5, 4000),
            ('2016-10-04', 90, 90, 100.18, 100.28, 4000),
            ('2016-10-05', 90, 90, 100.27, 100.43, 4000),
            ('2016-10-06', 90, 90, 100.29, 100.48, 5000),
            ('2016-10-07', 90, 90, 100.37, 100.48, 6000),
            ('2016-10-10', 90, 90, 100.55, 100.77, 3000),
            ('2016-10-11', 90, 90, 100.01, 100.16, 7000),
            ('2016-10-12', 90, 100, 100.11, 100.18, 11000)]

        data = pd.DataFrame.from_records(data, columns=labels)
        self.assertEqual(signal_is_volume_raising_within_check_days(data, check_days, raising_days), True)

        # h,h,h,h,h
        #file = test_filepath + 'test_isVolumeRaising_2_t1_HHHH.csv'
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-03', 90, 90, 100.39, 100.5, 4000),
            ('2016-10-04', 90, 90, 100.18, 100.28, 4000),
            ('2016-10-05', 90, 90, 100.27, 100.43, 4000),
            ('2016-10-06', 90, 90, 100.29, 100.48, 5000),
            ('2016-10-07', 90, 90, 100.37, 100.48, 6000),
            ('2016-10-10', 90, 90, 100.55, 100.77, 7000),
            ('2016-10-11', 90, 90, 100.01, 100.16, 8000),
            ('2016-10-12', 90, 100, 100.11, 100.18, 11000)]

        data = pd.DataFrame.from_records(data, columns=labels)
        self.assertEqual(signal_is_volume_raising_within_check_days(data, check_days, raising_days), True)

        ###########################
        # FALSE

        # t1: h, lowest, l, l, h but raising
        #file = test_filepath + 'test_isVolumeRaising_2_t1_HLowestLLL.csv'
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-03', 90, 90, 100.39, 100.5, 4000),
            ('2016-10-04', 90, 90, 100.18, 100.28, 4000),
            ('2016-10-05', 90, 90, 100.27, 100.43, 4000),
            ('2016-10-06', 90, 90, 100.29, 100.48, 5000),
            ('2016-10-07', 90, 90, 100.37, 100.48, 2000),
            ('2016-10-10', 90, 90, 100.55, 100.77, 3000),
            ('2016-10-11', 90, 90, 100.01, 100.16, 4000),
            ('2016-10-12', 90, 100, 100.11, 100.18, 11000)]

        data = pd.DataFrame.from_records(data, columns=labels)
        self.assertEqual(signal_is_volume_raising_within_check_days(data, check_days, raising_days), False)

        # t1: h, l, l, l, h
        #file = test_filepath + 'test_isVolumeRaising_2_t1_HLLLH.csv'
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-03', 90, 90, 100.39, 100.5, 4000),
            ('2016-10-04', 90, 90, 100.18, 100.28, 4000),
            ('2016-10-05', 90, 90, 100.27, 100.43, 4000),
            ('2016-10-06', 90, 90, 100.29, 100.48, 3000),
            ('2016-10-07', 90, 90, 100.37, 100.48, 3500),
            ('2016-10-10', 90, 90, 100.55, 100.77, 2300),
            ('2016-10-11', 90, 90, 100.01, 100.16, 2000),
            ('2016-10-12', 90, 100, 100.11, 100.18, 11000)]

        data = pd.DataFrame.from_records(data, columns=labels)
        self.assertEqual(signal_is_volume_raising_within_check_days(data, check_days, raising_days), False)

    def test_t2_is_last_volume_higher_than_avg__avg_not_higher__avg_is_higher(self):
        significance_factor = 1.2

        # t2: last 4k8, avg 4k --> below
        #file = test_filepath + 'test_t2_isLastVolumeHigherThanAvg_belowAvg4k_last3k8.csv'
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-03', 90, 90, 100.39, 100.5, 4000),
            ('2016-10-04', 90, 90, 100.18, 100.28, 4000),
            ('2016-10-05', 90, 90, 100.27, 100.43, 4000),
            ('2016-10-06', 90, 90, 100.29, 100.48, 4000),
            ('2016-10-07', 90, 90, 100.37, 100.48, 4000),
            ('2016-10-10', 90, 90, 100.55, 100.77, 4000),
            ('2016-10-11', 90, 90, 100.01, 100.16, 4000),
            ('2016-10-12', 90, 100, 100.11, 100.18, 3800)]

        data = pd.DataFrame.from_records(data, columns=labels)
        vol_avg = calc_avg_vol(data)
        self.assertEqual(signal_is_last_volume_higher_than_avg(data, vol_avg, significance_factor), False)

        # t2: above avg 4k2
        #file = test_filepath + 'test_t2_isLastVolumeHigherThanAvg_belowAvg4k_last5k2.csv'
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-03', 90, 90, 100.39, 100.5, 4000),
            ('2016-10-04', 90, 90, 100.18, 100.28, 4000),
            ('2016-10-05', 90, 90, 100.27, 100.43, 4000),
            ('2016-10-06', 90, 90, 100.29, 100.48, 4000),
            ('2016-10-07', 90, 90, 100.37, 100.48, 4000),
            ('2016-10-10', 90, 90, 100.55, 100.77, 4000),
            ('2016-10-11', 90, 90, 100.01, 100.16, 4000),
            ('2016-10-12', 90, 100, 100.11, 100.18, 5200)]

        data = pd.DataFrame.from_records(data, columns=labels)
        vol_avg = calc_avg_vol(data)
        self.assertEqual(signal_is_last_volume_higher_than_avg(data, vol_avg, significance_factor), True)

    def test_signal_is_a_few_higher_than_avg__higher__not_higher(self):
        check_days = 5
        raising_days = 3
        # T3: higher than avg
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-09-21', 90, 90, 100.35, 100.73, 4000),
            ('2016-09-22', 90, 90, 100.46, 100.73, 4000),
            ('2016-09-23', 90, 90, 100.54, 100.71, 4000),
            ('2016-09-26', 90, 90, 100.51, 100.73, 4000),
            ('2016-09-27', 90, 90, 100.41, 100.72, 4000),
            ('2016-09-28', 90, 90, 100.56, 100.75, 4000),
            ('2016-09-29', 90, 90, 100.16, 100.3, 4000),
            ('2016-09-30', 90, 90, 100.24, 100.8, 4000),
            ('2016-10-03', 90, 90, 100.39, 100.5, 4000),
            ('2016-10-04', 90, 90, 100.18, 100.28, 4000),
            ('2016-10-05', 90, 90, 100.27, 100.43, 4000),
            ('2016-10-06', 90, 90, 100.29, 100.48, 4000),
            ('2016-10-07', 90, 90, 100.37, 100.48, 4700),
            ('2016-10-10', 90, 90, 100.55, 100.77, 4800),
            ('2016-10-11', 90, 90, 100.01, 100.16, 4900),
            ('2016-10-12', 90, 100, 100.11, 100.18, 5000)]

        data = pd.DataFrame.from_records(data, columns=labels)
        vol_avg = calc_avg_vol(data)
        self.assertEqual(signal_is_a_few_higher_than_avg(data, check_days, raising_days, vol_avg), True)

        # T3: LOWER than avg
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-09-21', 90, 90, 100.35, 100.73, 4000),
            ('2016-09-22', 90, 90, 100.46, 100.73, 4000),
            ('2016-09-23', 90, 90, 100.54, 100.71, 4000),
            ('2016-09-26', 90, 90, 100.51, 100.73, 4000),
            ('2016-09-27', 90, 90, 100.41, 100.72, 4000),
            ('2016-09-28', 90, 90, 100.56, 100.75, 4000),
            ('2016-09-29', 90, 90, 100.16, 100.3, 4000),
            ('2016-09-30', 90, 90, 100.24, 100.8, 4000),
            ('2016-10-03', 90, 90, 100.39, 100.5, 4000),
            ('2016-10-04', 90, 90, 100.18, 100.28, 4000),
            ('2016-10-05', 90, 90, 100.27, 100.43, 4000),
            ('2016-10-06', 90, 90, 100.29, 100.48, 4500),
            ('2016-10-07', 90, 90, 100.37, 100.48, 3200),
            ('2016-10-10', 90, 90, 100.55, 100.77, 3800),
            ('2016-10-11', 90, 90, 100.01, 100.16, 2900),
            ('2016-10-12', 90, 100, 100.11, 100.18, 5000)]

        data = pd.DataFrame.from_records(data, columns=labels)
        vol_avg = calc_avg_vol(data)
        self.assertEqual(signal_is_a_few_higher_than_avg(data, check_days, raising_days, vol_avg), False)

    def test_signal_is_volume_raising(self):
        # True
        #file = test_filepath + 'test_isVolumeRaising_2_True.csv'

        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-03', 90, 90, 100.39, 100.5, 4000),
            ('2016-10-04', 90, 90, 100.18, 100.28, 4000),
            ('2016-10-05', 90, 90, 100.27, 100.43, 4000),
            ('2016-10-06', 90, 90, 100.29, 100.48, 5000),
            ('2016-10-07', 90, 90, 100.37, 100.48, 6000),
            ('2016-10-10', 90, 90, 100.55, 100.77, 7000),
            ('2016-10-11', 90, 90, 100.01, 100.16, 8000),
            ('2016-10-12', 90, 100, 100.11, 100.18, 11000)]

        data = pd.DataFrame.from_records(data, columns=labels)
        self.assertEqual(signal_is_volume_raising(data, 5, 3, 1.2), True)

        # False t1: volume not raising
        #file = test_filepath + 'test_isVolumeRaising_2_False_T1.csv'
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-03', 90, 90, 100.39, 100.5, 4000),
            ('2016-10-04', 90, 90, 100.18, 100.28, 4000),
            ('2016-10-05', 90, 90, 100.27, 100.43, 4000),
            ('2016-10-06', 90, 90, 100.29, 100.48, 5000),
            ('2016-10-07', 90, 90, 100.37, 100.48, 4900),
            ('2016-10-10', 90, 90, 100.55, 100.77, 4800),
            ('2016-10-11', 90, 90, 100.01, 100.16, 4750),
            ('2016-10-12', 90, 100, 100.11, 100.18, 4850)]

        data = pd.DataFrame.from_records(data, columns=labels)
        self.assertEqual(signal_is_volume_raising(data, 5, 3, 1.2), False)

        # False t2: last vol not higher than avg
        #file = test_filepath + 'test_isVolumeRaising_2_False_T2.csv'
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-03', 90, 90, 100.39, 100.5, 4000),
            ('2016-10-04', 90, 90, 100.18, 100.28, 4000),
            ('2016-10-05', 90, 90, 100.27, 100.43, 4000),
            ('2016-10-06', 90, 90, 100.29, 100.48, 5000),
            ('2016-10-07', 90, 90, 100.37, 100.48, 6000),
            ('2016-10-10', 90, 90, 100.55, 100.77, 6500),
            ('2016-10-11', 90, 90, 100.01, 100.16, 6750),
            ('2016-10-12', 90, 100, 100.11, 100.18, 3800)]

        data = pd.DataFrame.from_records(data, columns=labels)
        self.assertEqual(signal_is_volume_raising(data, 5, 3, 1.2), False)

        # False t3: at least NOT a few volume higher than avg
        #file = test_filepath + 'test_isVolumeRaising_2_False_T3.csv'
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-03', 90, 90, 100.39, 100.5, 4000),
            ('2016-10-04', 90, 90, 100.18, 100.28, 4000),
            ('2016-10-05', 90, 90, 100.27, 100.43, 4000),
            ('2016-10-06', 90, 90, 100.29, 100.48, 3400),
            ('2016-10-07', 90, 90, 100.37, 100.48, 3600),
            ('2016-10-10', 90, 90, 100.55, 100.77, 3700),
            ('2016-10-11', 90, 90, 100.01, 100.16, 3750),
            ('2016-10-12', 90, 100, 100.11, 100.18, 6800)]

        data = pd.DataFrame.from_records(data, columns=labels)
        self.assertEqual(signal_is_volume_raising(data, 5, 3, 1.2), False)

    def test_calculate_stopbuy_and_stoploss(self):
        #file = test_filepath + 'test_calculate_stopbuy_and_stoploss_Ok.csv'
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [
            ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
            ('2016-10-10', 23.62, 23.88, 23.55, 24.0, 44000),
            ('2016-10-11', 23.62, 30.0, 23.01, 23.16, 45000),
            ('2016-10-12', 23.16, 23.0, 23.11, 23.5, 46000)]

        data = pd.DataFrame.from_records(data, columns=labels)
        res = calculate_stopbuy_and_stoploss(data)
        # previous calculation with latest value should now be false
        self.assertEqual(np.math.isclose(res['sb'], 23.6175, abs_tol=0.001), False)  # =23,5*1.005
        self.assertEqual(np.math.isclose(res['sl'], 22.9089, abs_tol=0.001), False)  # =23,5*1.005*0.97

        # real calculation with real 52 w high value
        self.assertEqual(np.math.isclose(res['sb'], 30.15, abs_tol=0.001), True)  # =30*1.005
        self.assertEqual(np.math.isclose(res['sl'], 29.2455, abs_tol=0.001), True)  # =30*1.005*0.97

        # TODO using coverage: http://pymbook.readthedocs.io/en/latest/testing.html
        # https://blog.jetbrains.com/pycharm/2015/06/feature-spotlight-python-code-coverage-with-pycharm/
        # https://www.jetbrains.com/help/pycharm/configuring-code-coverage-measurement.html
        # https://www.jetbrains.com/help/pycharm/viewing-code-coverage-results.html


    # def test_read_current_day_from_yahoo(self):
    #
    #     names = ["ads", "ETR:GFT", "ETR:GFT", "AAPL", "AMZN"]
    #
    #     for name in names:
    #         data = read_current_day_from_yahoo(name)
    #         self.assertEqual(len(data), 1)
    #
    #     with self.assertRaises(Exception):
    #         read_current_day_from_yahoo("APPL.DE")

    # def test_read_data_from_google(self):
    #     end = datetime.now()
    #     ago52_w = (end - timedelta(weeks=52))
    #     ago2_w = (end - timedelta(weeks=2))
    #     res = read_data_from_google_with_pandas("ADBE", ago52_w, end) # 2017-09-21
    #     res = read_data_from_google_with_pandas("ADBE", ago52_w, end)  # 2017-09-210
    #     # TODO liefert immer 1 jahr
    #
    # def test_read_data_from_google_with_client(self):
    #     names = ["ads", "ETR:GFT", "ETR:GFT", "AAPL", "AMZN"]
    #
    #     for name in names:
    #         res = read_data_from_google_with_client(name)
    #         print()


    #def test_run_stock_screening_performance(self):
        # thr_start = datetime.now()
        # stocks_per_threads = 10
        # run_stock_screening(stocks_per_threads)
        # txt1 = "\nRuntime mit " + str(stocks_per_threads) +" Threads: " + str(datetime.now() - thr_start)
        #
        # thr_start = datetime.now()
        # stocks_per_threads = 5
        # run_stock_screening(stocks_per_threads)
        # txt2 = "\n\nRuntime mit " + str(stocks_per_threads) + " Threads: " + str(datetime.now() - thr_start)

        #thr_start = datetime.now()
        #stocks_per_threads = 2
        #run_stock_screening(stocks_per_threads)
        #txt3 = "\n\nRuntime mit " + str(stocks_per_threads) + " Threads: " + str(datetime.now() - thr_start)

        # print(txt1)
        # print(txt2)
        #print(txt3)
