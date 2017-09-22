import traceback
import datetime
import sys

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


