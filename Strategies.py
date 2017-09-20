import logging
from pandas_datareader import data
import pandas_datareader.data as web
from Utils import is_volume_high_enough, is_volume_raising, is52_w_high, write_stocks_to_buy_file, gap_up, \
    calculate_stopbuy_and_stoploss, get_current_function_name
from datetime import datetime, date, time
import pandas as pd


def replace_wrong_stock_market(stockName):
    replace_pattern = [".MU", ".DE", ".SW", ".F", ".EX", ".TI", ".MI"]

    for pattern in replace_pattern:
        if pattern in stockName:
            stockName = stockName.replace(pattern, "")
            stockName = "ETR:" + stockName
            break

    return stockName


def strat_scheduler(stock_names_to_check, data_provider, ago52_w, end):
    """
    function to schedule all strategien and return the stocks to buy
    :param stock_names_to_check: list with stock names to check
    :param data_provider: data provider to read stock data
    :param ago52_w: date and time 52weeks ago
    :param end: end date for read (today)
    :return: stocks to buy with {'buy', 'stock_name', 'sb', 'sl'}
    """

    stocks_to_buy = []  # stocks and enhanced data

    for stock_name in stock_names_to_check:
        read_exception = False

        try:
            # read data
            new_stock_name = replace_wrong_stock_market(stock_name)
            stock_name = new_stock_name
            stock52_w = data.DataReader(stock_name, data_provider, ago52_w.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))

        except Exception as e:
            print("strat_scheduler: Data Read exception: " + str(stock_name) + " is faulty: " + str(e))
            read_exception = True

        if not read_exception and len(stock52_w) > 0:
            ##############################################################
            # insert STRATEGIES here
            try:
                # TODO zusätzlicher vergleich zu DAX / NASDAQ vergleich handelsplus (titel trotz schwachem dax stark)
                res = strat_52_w_hi_hi_volume(stock_name, stock52_w, 5, 3, 1.2, 0.98)
                if res['buy'] == True and len(res) == 4:
                    stocks_to_buy.append({'buy': True, 'stock_name': res['stock_name'], 'sb': res['sb'], 'sl': res['sl']})
                    # print ("buy strat_52_w_hi_hi_volume: " + res)

                    # TODO canslim / Henkel

                    # TODO auswertung von chartsignalen mittels finanzen.at
                    # http://www.finanzen.net/chartsignale/index/Alle/liste/jc-1234er-long
                    ############################################################################

                    # else:
                    #     res = strat_gap_up__hi_volume(stock_name, stock52_w)
                    #     if res != "":
                    #         stocks_to_buy.append(res)
                    #         print ("buy strat_gap_up__hi_volume: " + res)
                    # TODO candlestick hammer
                    # res = strat_candlestick_hammer_HiVol (stock_name, stock52_w)

                    # TODO negativer hammer in den letzten 10 tagen als zeichen für nicht kaufen
                    # TODO zusätzliche reihung nach:
                    # - volumen anstieg stärke

                    # TODO http://www.finanzen.at/analysen

            except Exception as e:
                # e = sys.exc_info()[0]
                print("strat_scheduler: Strategy Exception: " + str(stock_name) + " is faulty: " + str(e))

                # if "Unable to read URL" in str(e):
                # return stocks_to_buy # return because google stops transfer

    return stocks_to_buy


def strat_52_w_hi_hi_volume(stock_name, stock52_w_data, check_days, min_cnt, min_vol_dev_fact, within52w_high_fact):
    """
    Check 52 week High, raising volume, and high enough volume

    :param  stock_name: name of the stock
    :param  stock52_w_data: stock data
    :param  check_days: number of days to check
    :param  min_cnt: min higher days within check days
    :param min_vol_dev_fact:
    :param within52w_high_fact:: factor current data within 52 w high (ex: currVal > (Max * 0.98))

    :return: stocks to buy with {'buy', 'stock_name', 'sb', 'sl'}
    """
    if stock_name is None or stock52_w_data is None or check_days is None or min_cnt is None or min_vol_dev_fact is None or within52w_high_fact is None:
        raise NotImplementedError

    if min_vol_dev_fact < 1:
        raise AttributeError("parameter min_vol_dev_fact must be higher than 1!")  # should above other avg volume

    if within52w_high_fact > 1:
        raise AttributeError("parameter within52w_high_fact must be lower than 1!")  # should above other avg volume

    if not is_volume_high_enough(stock52_w_data):
        return {'buy': False}

    if not is_volume_raising(stock52_w_data, check_days, min_cnt, min_vol_dev_fact):
        return {'buy': False}

    if not is52_w_high(stock52_w_data, within52w_high_fact):
        return {'buy': False}

    result = calculate_stopbuy_and_stoploss(stock52_w_data)

    return {'buy': True, 'stock_name': stock_name, 'sb': result['sb'], 'sl': result['sl'],
            'strategy_name': get_current_function_name()}


def strat_gap_up__hi_volume(stockName, stock52W):
    volumeHighEnough = False

    logging.debug(stockName)

    volumeHighEnough = is_volume_high_enough(stock52W)
    if volumeHighEnough:
        isGapUp = gap_up(stock52W, 1.03)

    if volumeHighEnough and isGapUp:
        dataLen = len(stock52W)

        #TODO change to new format {...}
        return stockName

    # else case
    return ""

    # def strat_candlestick_hammer_HiVol (stockName, stock52W):
    #     volumeHighEnough = False
    #
    #     logging.debug(stockName)
    #
    #     volumeHighEnough = is_volume_high_enough(stock52W)
    #     if volumeHighEnough:
    #         isHammer = hammer(stock52W, 1.02, 3)
    #
    #     if volumeHighEnough and isHammer:
    #         dataLen = len(stock52W)
    #         endKurs = stock52W.iloc[dataLen - 1].Close
    #         write_stocks_to_buy_file(
    #             str(stockName) + ", " + str(endKurs) + ", strat_gap_up__hi_volume")
    #         return stockName
    #
    #     # else case
    #     return ""
