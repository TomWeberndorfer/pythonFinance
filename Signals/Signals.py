import traceback

from Utils.CommonUtils import wrapper
from Utils.Logger_Instance import logger
from Utils.GlobalVariables import *
from Utils.StockDataUtils import calc_avg_vol
import talib
from talib import abstract

def signal_is_volume_raising_within_check_days(stock, check_days, min_cnt):
    """
    Checks, if the volume is rising within the check days, with at least minimum value.

    Args:
        stock: stock data
        check_days: number of days to check
        min_cnt: min raising days within check days

    Returns:
        True, if volume is raising

    Raises:
        NotImplementedError: if parameters are None

    """

    if stock is None or check_days is None or min_cnt is None:
        raise NotImplementedError

    data_len = len(stock)

    if data_len < 5: #must have enough data
        return None #TODO
        #TOD raise IndexError

    raise_cnt = 0
    i = check_days
    save_val = False
    while i > 0:
        try:
            vol_cur = stock.iloc[data_len - i][GlobalVariables.get_stock_data_labels_dict()['Volume']]
            if not save_val:
                if i is data_len:
                    vol_last = 0
                else:
                    vol_last = stock.iloc[data_len - i - 1][GlobalVariables.get_stock_data_labels_dict()['Volume']]
            if vol_cur > vol_last:
                raise_cnt += 1
                save_val = False
            else:
                save_val = True

        except Exception as e:
            logger.error("Unexpected Exception : " + str(e) + "\n" + str(traceback.format_exc()))

        i -= 1

    if raise_cnt < min_cnt:
        return None

    return True


def signal_is_last_volume_higher_than_avg(data, vol_avg, significance_factor):
    """
    Calculates the average and checks,
    if the last volume is higher than avg.

    Args:
        data: stock data
        vol_avg: average volume
        significance_factor:  is a factor to show that the cur vol is significantly higher


    Returns:
        True, if last volume higher than avg

    Raises:
        NotImplementedError: if parameters are None
    """
    if data is None or vol_avg is None or significance_factor is None:
        raise NotImplementedError
    data_len = len(data)

    if data_len < 5: #must have enough data
        return None  # TODO
        raise IndexError

    vol_last = data.iloc[data_len - 1][GlobalVariables.get_stock_data_labels_dict()['Volume']]
    min_calc_vol = vol_avg * significance_factor
    if vol_last < min_calc_vol:
        return None
    else:
        return True


def signal_is_a_few_higher_than_avg(stock, check_days, min_cnt, volume_average):
    """
    Calculates the average and checks,
    if the a few volume values are higher than avg.

    Args:
        stock: stock data
        check_days: number of days to check
        min_cnt: min higher days within check days
        volume_average: average volume

    Returns:
        True, if last volume higher than avg

    Raises:
        NotImplementedError: if parameters are None

    """
    if stock is None or check_days is None or min_cnt is None or volume_average is None:
        raise NotImplementedError

    # from [0] to end, without days to check above avg  ~ [datalen-15]
    cnt = check_days
    higher_than_avg = 0
    data_len = len(stock)

    if data_len < 5: #must have enough data
        return None  # TODO
        raise IndexError

    while cnt > 0:

        vol = stock.iloc[data_len - cnt][GlobalVariables.get_stock_data_labels_dict()['Volume']]
        if vol > volume_average:
            higher_than_avg += 1

        cnt -= 1

    if higher_than_avg >= min_cnt:
        return True

    return None


def signal_is_volume_raising(data, check_days, min_cnt, min_vol_dev_fact):
    """
        Uses functions, to check if stock is raising

        Args:
            data: stock data
            check_days: number of days to check
            min_cnt: min higher days within check days
            min_vol_dev_fact: factor current data within 52 w high (ex: currVal > (Max * 0.98))

        Returns:
            True, if raising

        Raises:
            NotImplementedError: if parameters are None
    """
    if data is None or check_days is None or min_cnt is None or min_vol_dev_fact is None:
        raise NotImplementedError

    if min_vol_dev_fact < 1:
        raise AttributeError("parameter min_vol_dev_fact must be higher than 1!")

    vol_avg = calc_avg_vol(data)

    # t1: minimum raising cnt within check days
    if not signal_is_volume_raising_within_check_days(data, check_days, min_cnt):
        return None

    # t2: last volume higher than avg
    # 1.2: is significant higher than avg
    if not signal_is_last_volume_higher_than_avg(data, vol_avg, min_vol_dev_fact):
        return None

    # t3: at least a few volume higher than avg
    if not signal_is_a_few_higher_than_avg(data, check_days, min_cnt, vol_avg):
        return None

    return True


def signal_is52_w_high(stock, within52w_high_fact=0.97):
    """
        Check 52 week High

        Args:
            stock: stock data
            within52w_high_fact: factor current data within 52 w high (ex: currVal > (Max * 0.98))
                                This is important when the maximum value is not the close value.
                                Therefore, highest value is taken for the maximum, and current value is not 52w high.

        Returns:
            True, if 52 week high

        Raises:
            NotImplementedError: if parameters are None
        """
    if stock is None or within52w_high_fact is None:
        raise NotImplementedError

    if within52w_high_fact > 1:
        raise AttributeError("parameter within52w_high_fact must be lower than 1!")  # should above other avg volume

    data_len = len(stock)

    if data_len < 5: #must have enough data
        return None  # TODO
        raise IndexError

    cur_val = stock.iloc[data_len - 1][GlobalVariables.get_stock_data_labels_dict()['High']]
    highest_high = stock[GlobalVariables.get_stock_data_labels_dict()['High']].max() #TODO  'Close', re-think

    if cur_val == highest_high:
        return True

    else:
        hi_minus_limit = highest_high * within52w_high_fact
        if cur_val >= hi_minus_limit:
            return True
        else:
            return None


def signal_gap_up(stock_data, min_gap_multiplier):
    """
        Check Gap Up strategy

        Args:
            stock_data: stock data
            min_gap_multiplier: multiplier gap up (percent to multiplier)

        Returns:
            True, if gap up

        Raises:
            NotImplementedError: if parameters are None
        """
    if stock_data is None or min_gap_multiplier is None:
        raise NotImplementedError

    data_len = len(stock_data)
    yesterday_val = stock_data.iloc[data_len - 2][GlobalVariables.get_stock_data_labels_dict()['Close']]
    cur_val = stock_data.iloc[data_len - 1][GlobalVariables.get_stock_data_labels_dict()['Open']]
    gap_up_val = (yesterday_val * min_gap_multiplier)
    # TODO: überprüfen ob tage hintereinander, achtung wochenende
    if cur_val > gap_up_val:
        return True
    else:
        return None


def signal_hammer(stock_data, hammer_length_in_factor, handle_bigger_than_head_factor):
    if stock_data is None or hammer_length_in_factor is None or handle_bigger_than_head_factor is None:
        raise NotImplementedError

    # TODO hammer bigger than AverageTrueRange

    # hammer head
    data_len = len(stock_data)
    close_value = stock_data.iloc[data_len - 1][GlobalVariables.get_stock_data_labels_dict()['Close']]
    yesterday_close_value = stock_data.iloc[data_len - 2][GlobalVariables.get_stock_data_labels_dict()['Close']]
    tday_open_value = stock_data.iloc[data_len - 1][GlobalVariables.get_stock_data_labels_dict()['Open']]
    tday_high_value = stock_data.iloc[data_len - 1][GlobalVariables.get_stock_data_labels_dict()['High']]
    tday_low_value = stock_data.iloc[data_len - 1][GlobalVariables.get_stock_data_labels_dict()['Low']]

    #do not use read hammer
    if tday_open_value > close_value:
        return None

    head_length = close_value - tday_open_value

    # handle
    if tday_open_value > close_value:
        return None

    handle_length = tday_open_value - tday_low_value

    # the handle must be bigger than handle to recognize a hammer
    if head_length > (handle_length * handle_bigger_than_head_factor):
        return None

    signal_len = head_length + handle_length

    # TODO use this instead: https://github.com/mrjbq7/ta-lib/tree/master/docs/func_groups
    #true_range = calc_true_range(tday_high_value, tday_low_value, yesterday_close_value)
    #TODO
    #true_range = ATR(tday_high_value, tday_low_value, yesterday_close_value, timeperiod=14)


    raise NotImplementedError  # TODO


def signal_is_volume_high_enough(historical_stock_data, min_req_vol=15000):
    """
    Checks, if the volume is high enough (liquid stock)
    :param historical_stock_data: historical stock data
    :param min_req_vol:  min volume for liquid stocks
    :return: true, if min volume requested
    """
    if historical_stock_data is None:
        raise NotImplementedError

    vol_avg = calc_avg_vol(historical_stock_data)

    if vol_avg > min_req_vol:
        return True
    else:
        return None


def evaluate_signals(signal_list, return_res=False):
    """
    Evaluates the signals from the signal list. Automatically wraps the list with function and all parameters.
    :return:
    """
    for entry in signal_list:
        func_str = entry.pop(0)

        if isinstance(func_str, str):
            try:
                func = eval(func_str)
            except Exception as e:
                func = abstract.Function(func_str)
        else:
            func = func_str  # argument is a func instead of string

        kwargs = None
        for e in entry:
            if isinstance(e, dict):
                kwargs = entry.pop()
                break

        if kwargs is None:
            res = wrapper(func, *entry)
        else:
            res = wrapper(func, *entry, **kwargs)
        if res is None or res is False:
            return None

    if return_res:
        return res
    else:
        return True
