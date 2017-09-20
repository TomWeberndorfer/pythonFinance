import pandas as pd
from pandas_datareader import data, wb
#import pandas.io.data as web  # Package and modules for importing data; this code may change depending on pandas version
import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import timedelta
import sys
import threading
from Utils import  is52_w_high, is_volume_high_enough, split_stock_list, is_volume_raising, is_volume_raising_within_check_days, \
    calc_avg_vol, is_last_volume_higher_than_avg, is_a_few_higher_than_avg, calculate_stopbuy_and_stoploss
from Strategies import strat_scheduler, strat_52_w_hi_hi_volume
import threading
import time
import logging
import pandas
import numpy as np
import pandas as pd
import unittest

filepath = 'C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\testData\\'

class MyTest(unittest.TestCase):

    def test_isVolumeHighEnough(self):
        #volume below 30k
        file = filepath + 'avg29k.csv'
        s_avg29k = pd.read_csv(file)
        self.assertEqual(is_volume_high_enough(s_avg29k), False)

        #volume above 30k
        file = filepath + 'avg31k.csv'
        s_avg31k = pd.read_csv(file)
        self.assertEqual(is_volume_high_enough(s_avg31k), True)

    def test_is52W_High(self):
        #last val 52 w Hi: data High: curVal is 100, other 90
        file = filepath + 'test_is52W_High_currHigh100_90others.csv'
        data = pd.read_csv(file)
        self.assertEqual(is52_w_high(data, 0.98), True)

        #last val < 0.98 hi: High: 100, lastval = 97
        file = filepath + 'test_is52W_High_curr97_100others.csv'
        data = pd.read_csv(file)
        self.assertEqual(is52_w_high(data, 0.98), False)

        #last val > 1.03 hi: High: 100, lastval = 104
        file = filepath + 'test_is52W_High_curr104_100others.csv'
        data = pd.read_csv(file)
        self.assertEqual(is52_w_high(data, 0.98), True)

        #last val = 99, High is 100
        file = filepath + 'test_is52W_High_curr99_100others.csv'
        data = pd.read_csv(file)
        self.assertEqual(is52_w_high(data, 0.98), True)

    def test_t1_isVolumeRaising_withinCheckDays(self):
        # t1: minimum raising
        # h,h,h,l,h
        file = filepath + 'test_isVolumeRaising_2_t1_HHHLH.csv'
        data = pd.read_csv(file)
        dataLen = len(data)
        self.assertEqual(is_volume_raising_within_check_days(data, 5, 3), True)

        #h,h,l,l,h
        file = filepath + 'test_isVolumeRaising_2_t1_HHLHH.csv'
        data = pd.read_csv(file)
        dataLen = len(data)
        self.assertEqual(is_volume_raising_within_check_days(data, 5, 3), True)

        #h,h,h,h,h
        file = filepath + 'test_isVolumeRaising_2_t1_HHHH.csv'
        data = pd.read_csv(file)
        dataLen = len(data)
        self.assertEqual(is_volume_raising_within_check_days(data, 5, 3), True)

        ###########################
        # FALSE

        #t1: h, lowest, l, l, h but raising
        file = filepath + 'test_isVolumeRaising_2_t1_HLowestLLL.csv'
        data = pd.read_csv(file)
        dataLen = len(data)
        self.assertEqual(is_volume_raising_within_check_days(data, 5, 3), False)

        #t1: h, l, l, l, h
        file = filepath + 'test_isVolumeRaising_2_t1_HLLLH.csv'
        data = pd.read_csv(file)
        dataLen = len(data)
        self.assertEqual(is_volume_raising_within_check_days(data, 5, 3), False)

    def test_t2_isLastVolumeHigherThanAvg(self):
        # t2: last 4k8, avg 4k --> below
        file = filepath + 'test_t2_isLastVolumeHigherThanAvg_belowAvg4k_last3k8.csv'
        data = pd.read_csv(file)
        vol_avg = calc_avg_vol(data, 5)
        self.assertEqual(is_last_volume_higher_than_avg(data, 5, vol_avg, 1.2), False)

        #t2: above avg 4k2
        file = filepath + 'test_t2_isLastVolumeHigherThanAvg_belowAvg4k_last5k2.csv'
        data = pd.read_csv(file)
        vol_avg = calc_avg_vol(data, 5)
        self.assertEqual(is_last_volume_higher_than_avg(data, 5, vol_avg, 1.2), True)

    def test_t3_is_a_few_higher_than_avg(self):

        #T3: higher than avg
        file = filepath + 'test_t3_is_a_few_higher_than_avg_AreHigher.csv'
        data = pd.read_csv(file)
        vol_avg = calc_avg_vol(data, 5)
        self.assertEqual(is_a_few_higher_than_avg(data, 5, 3, vol_avg), True)

        #T3: LOWER than avg
        file = filepath + 'test_t3_is_a_few_higher_than_avg_AreLower.csv'
        data = pd.read_csv(file)
        vol_avg = calc_avg_vol(data, 5)
        self.assertEqual(is_a_few_higher_than_avg(data, 5, 3, vol_avg), False)

    def test_isVolumeRaising_2(self):

        # True
        file = filepath + 'test_isVolumeRaising_2_True.csv'
        data = pd.read_csv(file)
        self.assertEqual(is_volume_raising(data, 5, 3, 1.2), True)

        #False t1: volume not raising
        file = filepath + 'test_isVolumeRaising_2_False_T1.csv'
        data = pd.read_csv(file)
        self.assertEqual(is_volume_raising(data, 5, 3, 1.2), False)

        # False t2: last vol not higher than avg
        file = filepath + 'test_isVolumeRaising_2_False_T2.csv'
        data = pd.read_csv(file)
        self.assertEqual(is_volume_raising(data, 5, 3, 1.2), False)

        # False t3: at least NOT a few volume higher than avg
        file = filepath + 'test_isVolumeRaising_2_False_T3.csv'
        data = pd.read_csv(file)
        self.assertEqual(is_volume_raising(data, 5, 3, 1.2), False)

    def test_strat_52WHi_HiVolume(self):
        file = filepath + 'test_strat_52WHi_HiVolume_1.csv'
        data = pd.read_csv(file)

        res = strat_52_w_hi_hi_volume("TestName1", data, 5, 3, 1.2, 0.98)
        num_of_return_params = len(res)
        self.assertEqual(num_of_return_params, 4)
        self.assertEqual(res['buy'], True)
        self.assertEqual(res['stock_name'], "TestName1")

        # volume higher, but stock value under 52w high within 98%
        file = filepath + 'test_strat_52WHi_HiVolume_Below52WHigh.csv'
        data = pd.read_csv(file)
        res = strat_52_w_hi_hi_volume("TestName1", data, 5, 3, 1.2, 0.98)
        num_of_return_params = len(res)
        self.assertEqual(num_of_return_params, 4)
        self.assertEqual(res['buy'], True)
        self.assertEqual(res['stock_name'], "TestName1")

        #test_strat_52WHi_HiVolume_Below52WHigh
        file = filepath + 'test_strat_52WHi_HiVolume_ErrorParameters.csv'
        data = pd.read_csv(file)
        res = strat_52_w_hi_hi_volume("TestName1", data, 5, 3, 1.2, 0.98)
        num_of_return_params = len(res)
        self.assertEqual(num_of_return_params, 4)
        self.assertEqual(res['buy'], True)
        self.assertEqual(res['stock_name'], "TestName1")

        file = filepath + 'test_strat_52WHi_HiVolume_VolumeNotAbove.csv'
        data = pd.read_csv(file)
        res = strat_52_w_hi_hi_volume("TestName1", data, 5, 3, 1.2, 0.98)
        num_of_return_params = len(res)
        self.assertEqual(num_of_return_params, 1)

        self.assertEqual(res['buy'], False)

        file = filepath + 'test_strat_52WHi_HiVolume_Not52WHigh.csv'
        data = pd.read_csv(file)
        res = strat_52_w_hi_hi_volume("TestName1", data, 5, 3, 1.2, 0.98)
        num_of_return_params = len(res)
        self.assertEqual(num_of_return_params, 1)
        self.assertEqual(res['buy'], False)

        with self.assertRaises(AttributeError):
            strat_52_w_hi_hi_volume("TestName1", data, 5, 3, 0.98, 0.98)
            strat_52_w_hi_hi_volume("TestName1", data, 5, 3, 1.2, 1.2)

    def test_calculate_stopbuy_and_stoploss(self):
        file = filepath + 'test_calculate_stopbuy_and_stoploss_Ok.csv'
        data = pd.read_csv(file)
        res = calculate_stopbuy_and_stoploss(data)
        self.assertEqual(np.math.isclose(res['sb'], 23.6175, abs_tol=0.001), True) #=23,5*1.005
        self.assertEqual(np.math.isclose(res['sl'], 22.9089, abs_tol=0.001), True)  # =23,5*1.005*0.97

        #TODO using coverage: http://pymbook.readthedocs.io/en/latest/testing.html
        #https://blog.jetbrains.com/pycharm/2015/06/feature-spotlight-python-code-coverage-with-pycharm/
        # https://www.jetbrains.com/help/pycharm/configuring-code-coverage-measurement.html
        # https://www.jetbrains.com/help/pycharm/viewing-code-coverage-results.html




