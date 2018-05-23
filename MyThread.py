import threading
import traceback
import datetime
import sys
import os
from abc import abstractmethod

from Utils.common_utils import split_list, get_current_function_name

#TODO uebergeben statt filepath can be none
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MyThread:
    def __init__(self, num_of_stocks_per_thread):
        self.thrToExe = []
        self.threads = []
        self.filepath = ROOT_DIR #TODO uebergabe
        self.num_of_stocks_per_thread = num_of_stocks_per_thread

    def _execute_threads(self):

        # Start new Threads
        thr_start = datetime.datetime.now()

        for tr in self.thrToExe:
            try:
                if tr is not None:
                    tr.start()
                    print("Thread started:" + str(tr))
                    self.threads.append(tr)

            except Exception as e:
                sys.stderr.write("EXCEPTION _execute_threads: " + str(e) + "\n")
                traceback.print_exc()

        # Wait for all threads to complete
        # TODO performance tests
        for t in self.threads:
            t.join()

        txt = "Runtime Threads " + str(get_current_function_name()) + ": " + str(
            datetime.datetime.now() - thr_start) + ", cnt of threads: " + str(len(self.threads))
        print(txt)

    def _append_list(self, list_to_execute):
        split_sub_list = split_list(list_to_execute, self.num_of_stocks_per_thread)
        for sub_list in split_sub_list:
            self._append_thread(
                threading.Thread(target=self._method_to_execute,
                                 kwargs={'stock_data_container_sub_list': sub_list}))

    def _append_thread(self, thread_to_append):
        try:
            if thread_to_append is not None:
                self.thrToExe.append(thread_to_append)
        except Exception as e:
            sys.stderr.write("EXCEPTION _append_thread: " + str(e) + "\n")
            traceback.print_exc()

    @abstractmethod
    def _method_to_execute(self, sub_list):
        raise NotImplementedError ("Abstract Method!!")


