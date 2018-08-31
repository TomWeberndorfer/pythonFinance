# var.py

from pandas import DataFrame

from Utils.GlobalVariables import *
from Utils.StockDataUtils import value_at_risk

if __name__ == "__main__":
    labels = []
    for key, value in GlobalVariables.get_stock_data_labels_dict(False).items():
        labels.append(value)

    data = [
        ('2016-09-30', 23.35, 23.91, 23.24, 23.8, 31800),
        ('2016-10-03', 23.68, 23.69, 23.39, 23.5, 31600),
        ('2016-10-04', 23.52, 23.64, 23.18, 23.28, 31700),
        ('2016-10-05', 23.28, 23.51, 23.27, 23.43, 31500),
        ('2016-10-06', 23.38, 23.56, 23.29, 23.48, 42000),
        ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
        ('2016-10-10', 23.62, 23.88, 23.55, 23.77, 44000),
        ('2016-10-11', 23.62, 23.74, 23.01, 23.16, 45000),
        ('2016-10-12', 26.16, 27, 26.11, 26, 46000),
        ('2016-10-13', 23.52, 23.64, 23.18, 23.238, 32000),
        ('2016-10-14', 23.52, 23.64, 23.18, 23.0, 33000),
        ('2016-10-15', 18.7, 20, 17, 18.5, 33000),
        ('2016-10-16', 18, 19, 16, 15, 33000)]

    df = DataFrame.from_records(data, columns=labels)
    P = 2500
    c = 0.99  # 99% confidence interval

    var = value_at_risk(df["close"], P, c)
    print("Value-at-Risk: $%0.2f" % var)
