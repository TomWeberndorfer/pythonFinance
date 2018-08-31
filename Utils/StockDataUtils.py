import numpy
import numpy as np
import pandas as pd
from scipy.stats import norm

from Utils.GlobalVariables import GlobalVariables


def calc_avg_vol(stock_data):
    """
    Calculates the average volume of stock data except the days to skip from end.
    :param stock_data: stock data
    :return: Average Value
    """

    if stock_data is None or len(stock_data) <= 0:
        raise NotImplementedError

    vol_avg = stock_data[GlobalVariables.get_stock_data_labels_dict()["Volume"]].mean()
    return vol_avg


def calculate_stopbuy_and_stoploss(stock_data, stop_buy_limit_percent=1.005, stop_loss_limit_percent=0.97):
    """
    calculates stop buy and stop loss values
    :param stop_loss_limit_percent: stop loss 3% lower than stop buy
    :param stop_buy_limit_percent: stop buy 0,5% higher than last val
    :param stock_data: 52w stock data
    :return: stop buy and stop loss: {'sb':sb, 'sl': sl}
    """

    if stock_data is None:
        raise NotImplementedError

    if len(stock_data) <= 0:
        return {'stop_buy': 0, 'stop_loss': 0}

    # values should be calc with max (real 52wHigh)
    highest_high = stock_data[GlobalVariables.get_stock_data_labels_dict()['High']].max()
    sb = highest_high * stop_buy_limit_percent  # stop buy 0,5% higher than last val
    sl = sb * stop_loss_limit_percent  # stop loss 3% lower than stop buy

    return {'stop_buy': sb, 'stop_loss': sl}


def calc_true_range(tday_high_value, tday_low_value, yesterday_close_value):
    """
    # max of todays high - low, abs(high - yday close), abs (low - yday Close)
    :param tday_high_value:
    :param tday_low_value:
    :param yesterday_close_value:
    :return:
    """

    today_high_low = tday_high_value - tday_low_value
    high_yday_close = abs(tday_high_value - yesterday_close_value)
    low_yday_close = abs(tday_low_value - yesterday_close_value)

    true_range = max(today_high_low, high_yday_close, low_yday_close)

    return true_range


def calc_mean_true_range(stock_data):
    """
    TODO replace with atr?
    :param stock_data:
    :return:
    """
    tr = []
    i = 0
    while i < len(stock_data):
        yesterday_close_value = stock_data.iloc[i - 1][GlobalVariables.get_stock_data_labels_dict()['Close']]
        tday_high_value = stock_data.iloc[i][GlobalVariables.get_stock_data_labels_dict()['High']]
        tday_low_value = stock_data.iloc[i][GlobalVariables.get_stock_data_labels_dict()['Low']]
        tr.append(calc_true_range(tday_high_value, tday_low_value, yesterday_close_value))

        i += 1

    return numpy.mean(tr)


def convert_backtrader_to_dataframe(data):
    """
    Convert the backtrader data to the dataframe data.
    :param data: backtrader data
    :return: pandas data frame
    """
    cols = []
    for key, value in GlobalVariables.get_stock_data_labels_dict().items():
        cols.append(value)
    lst = []
    cols = ['open', 'high', 'low', 'close', 'volume']

    # the data starts at [0] with the current value
    # and goes negative for older values
    i = - len(data.open) + 1
    while i <= 0:
        try:
            lst.append([
                # data.datetime[i],
                float(data.open[i]),
                float(data.high[i]),
                float(data.low[i]),
                float(data.close[i]),
                float(data.volume[i])])
        except Exception as e:
            # nothing to do
            break
        i += 1

    df1 = pd.DataFrame(lst, columns=cols)

    return df1


def value_at_risk(df_close, portfolio_value, conv=0.99):
    per_change = df_close.pct_change()
    mu = np.mean(per_change)
    sigma = np.std(per_change)

    var = var_cov_var(portfolio_value, conv, mu, sigma)
    return var


def var_cov_var(P, c, mu, sigma):
    """
    Variance-Covariance calculation of daily Value-at-Risk
    using confidence level c, with mean of returns mu
    and standard deviation of returns sigma, on a portfolio
    of value P.
    """
    alpha = norm.ppf(1 - c, mu, sigma)
    return P - P * (alpha + 1)
