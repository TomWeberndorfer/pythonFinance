import unittest

import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta



from Strategies import strat_52_w_hi_hi_volume

program_start_time = datetime.now()
filepath = 'C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\testData\\'

file = filepath + 'AAPL.csv'
data = pd.read_csv(file)


file = filepath + 'ACN.csv'
data2 = pd.read_csv(file)



res = strat_52_w_hi_hi_volume("TestName1", data, 5, 3, 1.2, 0.98)
res = strat_52_w_hi_hi_volume("TestName2", data2, 5, 3, 1.2, 0.98)



print("INFO: runtime " + str(
    datetime.now() - program_start_time))