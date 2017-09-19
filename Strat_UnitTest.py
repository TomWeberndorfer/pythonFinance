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
from Utils import  is52W_High, isVolumeHighEnough, splitStockList, isVolumeRaising_2, isVolumeRaising_withinCheckDays
from Strategies import strat_scheduler
import threading
import time
import logging
import pandas
import numpy as np
import pandas as pd
import unittest



exitFlag = 0
threads = []
stocksToBuy = []
err = []

filepath = 'C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\testData\\'
    # todo for unit tests
    # stock52W.to_csv('C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\out.csv')
#stockTest = pd.read_csv('C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\out.csv')


class MyTest(unittest.TestCase):

    def test_isVolumeHighEnough(self):
        #volume below 30k
        file = filepath + 'avg29k.csv'
        s_avg29k = pd.read_csv(file)
        self.assertEqual(isVolumeHighEnough(s_avg29k, 10), False)

        #volume above 30k
        file = filepath + 'avg31k.csv'
        s_avg31k = pd.read_csv(file)
        self.assertEqual(isVolumeHighEnough(s_avg31k, 10), True)

    def test_is52W_High(self):
        #last val 52 w Hi: data High: curVal is 100, other 90
        file = filepath + 'test_is52W_High_currHigh100_90others.csv'
        data = pd.read_csv(file)
        self.assertEqual(is52W_High(data), True)

        #last val < 0.98 hi: High: 100, lastval = 97
        file = filepath + 'test_is52W_High_curr97_100others.csv'
        data = pd.read_csv(file)
        self.assertEqual(is52W_High(data), False)

        #last val > 1.03 hi: High: 100, lastval = 104
        file = filepath + 'test_is52W_High_curr104_100others.csv'
        data = pd.read_csv(file)
        self.assertEqual(is52W_High(data), True)

        #last val = 99, High is 100
        file = filepath + 'test_is52W_High_curr99_100others.csv'
        data = pd.read_csv(file)
        self.assertEqual(is52W_High(data), True)

    def test_isVolumeRaising_withinCheckDays(self):
        # t1: minimum raising
        # h,h,h,l,h
        file = filepath + 'test_isVolumeRaising_2_t1_HHHLH.csv'
        data = pd.read_csv(file)
        dataLen = len(data)
        self.assertEqual(isVolumeRaising_withinCheckDays(data, 5, 3, dataLen), True)


        #t1: h, lowest, l, l, h but raising
        file = filepath + 'test_isVolumeRaising_2_t1_HLowestLLL.csv'
        data = pd.read_csv(file)
        dataLen = len(data)
        self.assertEqual(isVolumeRaising_withinCheckDays(data, 5, 3, dataLen), False)

        #h,h,l,l,h

        #h,h,h,h,h

    def test_isVolumeRaising_2(self):
        #t1: minimum raising
        #h,h,h,l,h
        file = filepath + 'test_isVolumeRaising_2_t1_HHHLH.csv'
        data = pd.read_csv(file)
        #self.assertEqual(isVolumeRaising_2(data), True)

        #t2: average last

        #t3:

        #raising 4 days

        # raising 2 days

        # raising 2 days 1 down, 7 raising
