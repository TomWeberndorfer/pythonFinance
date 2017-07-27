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
from Utils import isVolumeRaising, is52W_High, isVolumeHighEnough, splitStockList
from Strategies import strat_52WHi_HiVolume
import threading
import time
import logging
import pandas
import numpy as np
import pandas as pd


exitFlag = 0
threads = []
stocksToBuy = []
err = []

#stocksToBuy = strat_52WHi_HiVolume(self.stocksToCheck, dataProvider, Ago52W, Ago5D, end)

d = {'a' : 0., 'b' : 1., 'c' : 2.}
pd.Series(d)
stock = {}

i = 0
while i < 2:
    stock["Volume"] = 3