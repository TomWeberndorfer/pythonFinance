import traceback

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
from Utils import is52_w_high, is_volume_high_enough, split_stock_list, get_symbol_from_name_from_yahoo, \
    get52_w__h__symbols__from_excel, \
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

        for tr in self.thrToExe:
            try:
                if tr is not None:
                    tr.start()
                    self.threads.append(tr)

            except Exception as e:
                sys.stderr.write("EXCEPTION execute_threads: " + str(e) + "\n")
                traceback.print_exc()

        # Wait for all threads to complete
        for t in self.threads:
            t.join()

        print("Runtime Threads " + str(self.name) + ": " + str(
            datetime.datetime.now() - thr_start) + ", cnt of threads: " + str(len(self.threads)))

    def append_thread(self, thread_to_append):
        try:
            if thread_to_append is not None:
                self.thrToExe.append(thread_to_append)
        except Exception as e:
            sys.stderr.write("EXCEPTION append_thread: " + str(e) + "\n")
            traceback.print_exc()


