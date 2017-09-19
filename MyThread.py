import pandas as pd
from pandas_datareader import data, wb
# import pandas.io.data as web  # Package and modules for importing data; this code may change depending on pandas version
import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import timedelta
import sys
import threading
from Utils import is52W_High, isVolumeHighEnough, splitStockList, getSymbolFromName, \
    get52W_H_Symbols_FromExcel, \
    write_stocks_to_buy_file
from Strategies import strat_scheduler
import threading
import time
import logging

##########################################################
class MyThread:
    def __init__(self, name):
        self.name = name
        self.thrToExe = []
        self.threads = []

    def execute_threads(self):

        # Start new Threads
        thr_start = datetime.datetime.now()

        trCntr = 0

        for tr in self.thrToExe:
            try:
                if tr is not None:
                    tr.start()
                    trCntr += 1
                    self.threads.append(tr)


            except Exception as e:
                print("EXCEPTION execute_threads: " + str(e))

        # Wait for all threads to complete
        for t in self.threads:
            t.join()

        print("Runtime Threads " + str(self.name) + ": " + str(
            datetime.datetime.now() - thr_start) + ", cnt of threads: " + str(trCntr))

    def append_thread(self, thread_to_append):
        try:
            if thread_to_append is not None:
                self.thrToExe.append(thread_to_append)
        except Exception as e:
            print("EXCEPTION append_thread: " + str(e))


