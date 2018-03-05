import sys
import traceback

from DataRead_Google_Yahoo import get_ticker_data_with_webreader
from Signals import signal_is_volume_raising, signal_is52_w_high, signal_gap_up, signal_hammer, \
    signal_is_volume_high_enough
from Utils.common_utils import calculate_stopbuy_and_stoploss, get_current_function_name

#TODO as parameter
filepath = 'C:\\temp\\'


def strat_scheduler(stock_names_to_check, ago52_w, end, params):
    """
    function to schedule all strategies and return the stocks to buy
    :param params: parameter for strategy within structure: {'strat_52_w_hi_hi_volume': {'check_days': 5, 'min_cnt': 3, 'min_vol_dev_fact': 1.1, 'within52w_high_fact': 0.98}}
    :param stock_names_to_check: list with stock names to check
    :param ago52_w: date and time 52weeks ago
    :param end: end date for read (today)
    :return: stocks to buy with {'buy', 'stock_name', 'sb', 'sl'}
    """

    stocks_to_buy = []  # stocks and enhanced data

    for stock_name in stock_names_to_check:
        read_exception = False

        try:
            # read data
            #TODO
            #stock52_w = read_data_from_google_with_pandas(stock_name, ago52_w, end)
            #stock52_w = get_data_from_google_with_webreader (stock_name,  filepath + 'stock_dfs', False, False)
            stock52_w = get_ticker_data_with_webreader(stock_name, filepath + 'stock_dfs', 'yahoo', False, False)

        except Exception as e:
            # traceback.print_exc()
            print("strat_scheduler: Data Read exception: " + str(stock_name) + " is faulty: " + str(e))
            read_exception = True

        if not read_exception and len(stock52_w) > 0:
            #print(" try with " + str(stock_name))
            ##############################################################
            # insert STRATEGIES here
            try:
                # TODO zusätzlicher vergleich zu DAX / NASDAQ vergleich handelsplus (titel trotz schwachem dax stark)
                str_52w_p = params[0]
                check_days = str_52w_p['check_days']
                min_cnt = str_52w_p['min_cnt']
                min_vol_dev_fact = str_52w_p['min_vol_dev_fact']
                within52w_high_fact = str_52w_p['within52w_high_fact']
                res = strat_52_w_hi_hi_volume(stock_name, stock52_w, check_days, min_cnt, min_vol_dev_fact, within52w_high_fact)
                if res['buy']:
                    stocks_to_buy.append(
                        {'buy': True, 'stock_name': res['stock_name'], 'sb': res['sb'], 'sl': res['sl'], 'strategy_name': res['strategy_name'], 'params': params[0], 'data': stock52_w})

                    # TODO canslim / Henkel
                    # TODO text auswertung http://www.learndatasci.com/python-finance-part-3-moving-average-trading-strategy/
                    # TODO auswertung von chartsignalen mittels finanzen.at
                    # http://www.finanzen.net/chartsignale/index/Alle/liste/jc-1234er-long
                    ############################################################################

                # else:
                #     str_gap_up_p = params[1]
                #     min_gap_factor = str_gap_up_p['min_gap_factor']
                #     # add data from today for gap up
                #     #TODO must check if late and google adds itself
                #     res = strat_gap_up__hi_volume(stock_name, stock52_w, min_gap_factor)
                #     if res['buy']:
                #          stocks_to_buy.append(
                #              {'buy': True, 'stock_name': res['stock_name'], 'sb': res['sb'], 'sl': res['sl'],
                #               'strategy_name': res['strategy_name'], 'params': params[1]})

                    # else :
                    #     str_52w_p = params[2]
                    #     hammer_length_in_factor = str_52w_p['hammer_length_in_factor']
                    #     handle_bigger_than_head_factor = str_52w_p['handle_bigger_than_head_factor']
                    #     res = strat_candlestick_hammer_hi_vol(stock_name, stock52_w, hammer_length_in_factor, handle_bigger_than_head_factor)
                    #     if res['buy']:
                    #         stocks_to_buy.append(
                    #             {'buy': True, 'stock_name': res['stock_name'], 'sb': res['sb'], 'sl': res['sl'],
                    #              'strategy_name': res['strategy_name'], 'params': params[1]})
                    # TODO candlestick signal_hammer

                    # TODO negativer signal_hammer in den letzten 10 tagen als zeichen für nicht kaufen
                    # TODO zusätzliche reihung nach:
                    # - volumen anstieg stärke

                    # TODO http://www.finanzen.at/analysen
                    # TODO ansehen: https://www.youtube.com/watch?v=IuhLfRJTHmY

            except Exception as e:
                # e = sys.exc_info()[0]
                sys.stderr.write(
                    "strat_scheduler: Strategy Exception: " + str(stock_name) + " is faulty: " + str(e) + "\n")
                traceback.print_exc()

                # if "Unable to read URL" in str(e):
                # return stocks_to_buy # return because google stops transfer
    print("Finished with [" + str(stock_names_to_check) + "]")
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

    :return: stock to buy with {'buy', 'stock_name', 'sb', 'sl'}
    """
    if stock_name is None or stock52_w_data is None or check_days is None or min_cnt is None or min_vol_dev_fact is None or within52w_high_fact is None:
        raise NotImplementedError

    if min_vol_dev_fact < 1:
        raise AttributeError("parameter min_vol_dev_fact must be higher than 1!")  # should above other avg volume

    if within52w_high_fact > 1:
        raise AttributeError("parameter within52w_high_fact must be lower than 1!")  # should above other avg volume

    if not signal_is_volume_high_enough(stock52_w_data):
        return {'buy': False}

    if not signal_is_volume_raising(stock52_w_data, check_days, min_cnt, min_vol_dev_fact):
        return {'buy': False}

    if not signal_is52_w_high(stock52_w_data, within52w_high_fact):
        return {'buy': False}

    result = calculate_stopbuy_and_stoploss(stock52_w_data)

    return {'buy': True, 'stock_name': stock_name, 'sb': result['sb'], 'sl': result['sl'],
            'strategy_name': get_current_function_name()}


def strat_gap_up__hi_volume(stock_name, stock_data, min_gap_factor):
    """
    Strategy with gap between last and open and high volume

    :param stock_name: stock name
    :param stock_data: stock data
    :param min_gap_factor: minimum gap up factor (ex: 1.03 = 3%)
    :return: stock to buy with {'buy', 'stock_name', 'sb', 'sl'}
    """

    if stock_name is None or stock_data is None or min_gap_factor is None:
        raise NotImplementedError

    if not signal_is_volume_high_enough(stock_data):
        return {'buy': False}

    if not signal_gap_up(stock_data, min_gap_factor):
        return {'buy': False}

    result = calculate_stopbuy_and_stoploss(stock_data)

    return {'buy': True, 'stock_name': stock_name, 'sb': result['sb'], 'sl': result['sl'],
            'strategy_name': get_current_function_name()}


def strat_candlestick_hammer_hi_vol (stock_name, stock_data, hammer_length_in_factor, handle_bigger_than_head_factor):
    if stock_name is None or stock_data is None or hammer_length_in_factor is None or handle_bigger_than_head_factor is None:
        raise NotImplementedError

    if not signal_is_volume_high_enough(stock_data):
        return {'buy': False}

    if not signal_hammer(stock_data, hammer_length_in_factor, handle_bigger_than_head_factor):
        return {'buy': False}

    result = calculate_stopbuy_and_stoploss(stock_data)

    return {'buy': True, 'stock_name': stock_name, 'sb': result['sb'], 'sl': result['sl'],
             'strategy_name': get_current_function_name()}