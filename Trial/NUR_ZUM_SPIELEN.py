import pandas as pd
import os
import quandl
import time
from datetime import datetime
auth_tok = 'Gq6_HqRdHa8KWKV4r7-F'
start_time = datetime.now()
data = quandl.get("WIKI/AAPL", trim_start = "2014-12-12", trim_end = "2014-12-30", authtoken=auth_tok)

end_time = datetime.now()
time_diff = end_time - start_time
print("Time to get the stocks:" + (str(time_diff)))

#print(data)