import logging
from pandas_datareader import data
import pandas_datareader.data as web
from Utils import is_volume_high_enough, is_volume_raising, is52_w_high, write_stocks_to_buy_file, gap_up, \
    calculate_stopbuy_and_stoploss, get_current_function_name
from datetime import datetime, date, time
import pandas as pd


import sys

# for current func name, specify 0 or no argument.
# for name of caller of current func, specify 1.
# for name of caller of caller of current func, specify 2. etc.
#currentFuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name


#def testFunction():
    #print ("You are in function:", currentFuncName())
    #print ("This function's caller was:", currentFuncName(1))


def invokeTest():
   return get_current_function_name()


print(str(invokeTest()))