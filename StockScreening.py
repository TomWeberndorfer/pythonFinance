import threading
import traceback
from datetime import datetime
from datetime import timedelta
import sys

from DataRead_Google_Yahoo import get52_w__h__symbols__from_excel, __get_symbol_from_name_from_yahoo
from MyThread import MyThread
from Strategies import strat_scheduler
from Utils import split_list, print_stocks_to_buy, plot_stock_as_candlechart_with_volume, append_to_file, \
    read_tickers

threads = []
stocks_to_buy = []
err = []
program_start_time = datetime.now()
params = []


# TODO maybe move to better place
def function_for_threading_strat_scheduler(stock_names_to_check, ago52_w_time, end_l):
    print("Started with: " + str(stock_names_to_check))

    stocks_to_buy.extend(strat_scheduler(stock_names_to_check, ago52_w_time, end_l, params))


def plot_stocks_to_buy_as_candlechart_with_volume(stocks_to_buy, start_date, end_date):
    """
    plots alist with stock names
    :param stocks_to_buy:
    :param start_date:
    :param end_date:
    :return:
    """
    for stock in stocks_to_buy:
        try:
            stock_name = stock['stock_name']
            # TODO weg
            # stock_data = read_data_from_google_with_pandas(stock_name, start_date, end_date)
            stock_data = stock['data']
            plot_stock_as_candlechart_with_volume(stock_name, stock_data)

        except Exception as e:
            sys.stderr.write("EXCEPTION execute_threads: " + str(e) + "\n")
            traceback.print_exc()


def run_stock_screening():
    try:
        # threads = []
        # stocks_to_buy = []
        # err = []
        # program_start_time = datetime.now()
        # params = []

        ##########################
        # config
        num_of_stocks_per_thread = 20
        volume_day_delta = 5
        volume_avg_day_delta = 15
        end = datetime.now()
        ago52_w = (end - timedelta(weeks=52))

        data_provider = "google"  # TODO
        filepath = 'C:\\temp\\'
        stock_list_name = "stockList.txt"
        stocks_to_buy_name = "StocksToBuy.CSV"
        excel_file_name = '52W-HochAutomatisch_Finanzen.xlsx'
        tickers_file_name = "stock_tickers.pickle"
        stocknames_file_name = "stock_names.pickle"
        tickers_file = filepath + tickers_file_name
        stocknames_file = filepath + stocknames_file_name

        # enhanced stock messages:
        # logging.basicConfig(level=logging.DEBUG)

        ##########################

        # symbols to read
        nasdaq100__symbols = ["AAPL", "ADBE", "ADI", "ADP", "ADSK", "AKAM", "ALXN",
                              "AMAT", "AMGN", "AMZN", "ATVI", "AVGO", "BBBY", "BIDU", "BIIB",
                              "CA", "CELG", "CERN", "CHKP", "CHRW", "CHTR", "CMCSA",
                              "COST", "CSCO", "CTSH", "CTXS", "DISCA", "DISCK", "DISH",
                              "DLTR", "EBAY", "EQIX", "ESRX", "EXPD", "EXPE", "FAST",
                              "FB", "FFIV", "FISV", "FOXA", "GILD", "GOOG",
                              "GRMN", "HSIC", "ILMN", "INTC", "INTU", "ISRG", "KLAC",
                              "LBTYA", "LLTC", "LMCK", "LVNTA", "MAR", "MAT", "MDLZ",
                              "MNST", "MSFT", "MU", "MXIM", "MYL", "NFLX", "NTAP", "NVDA",
                              "NXPI", "ORLY", "PAYX", "PCAR", "PCLN", "QCOM", "QVCA", "REGN",
                              "ROST", "SBAC", "SBUX", "SIRI", "SPLS", "SRCL",
                              "STX", "SYMC", "TRIP", "TSCO", "TSLA", "TXN", "VIAB", "VIP",
                              "VOD", "VRSK", "VRTX", "WDC", "WFM", "WYNN", "XLNX", "YHOO", "NOC"]

        dax_symbols = ["ETR:ADS", "ETR:ALV", "ETR:BAS", "ETR:BMW", "ETR:CBK", "ETR:CON", "ETR:DAI",
                       "ETR:DB1", "ETR:DBK", "FRA:DPW", "ETR:DPW", "ETR:DTE", "ETR:FME", "ETR:HEN3",
                       "ETR:IFX", "ETR:LHA", "ETR:LIN", "ETR:MAN", "ETR:MRK", "ETR:MUV2",
                       "ETR:RWE", "ETR:SAP", "ETR:SIE", "ETR:TKA", "ETR:TUI1", "ETR:VOW", "ETR:BAYN",
                       "ETR:FNTN", "ETR:O2D", "ETR:QIA", "ETR:DRI", "ETR:AM3D", "ETR:O1BC", "ETR:GFT", "ETR:NDX1",
                       "ETR:SBS", "ETR:COK", "ETR:DLG", "ETR:DRW3", "ETR:SMHN", "ETR:WDI", "ETR:BC8", "ETR:MOR",
                       "ETR:SOW", "ETR:AIXA", "ETR:ADV", "ETR:PFV", "ETR:JEN", "ETR:AFX", "ETR:UTDI", "ETR:NEM",
                       "ETR:SRT3",
                       "ETR:EVT", "ETR:WAF", "ETR:RIB", "ETR:S92", "ETR:COP", "ETR:TTR1", "ETR:SZG", "ETR:VT9",
                       "VIE:SEM"]  # TODO vienna

        all_symbols = []
        all_names = []

        ###############################################################################################
        # enter stock filter options
        # 0 = ALL
        # 1 = DAX
        # 2 = NASDAQ
        # 3 = finanzen excel
        # 4 = DAX, NASDAQ , S&P500
        # 5 = S&P500
        option = 5

        # params for strat_52_w_hi_hi_volume
        params.append({'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98})

        # params for strat_gap_up__hi_volume
        params.append({'min_gap_factor': 1.03})

        # strat_candlestick_hammer_hi_vol
        params.append({'hammer_length_in_factor': 1.01, 'handle_bigger_than_head_factor': 2})
        ###########################################################

        # DAX
        if option == 1:
            symbol = __get_symbol_from_name_from_yahoo ("Aixtron", "de")
            dax_symbols = [symbol]
            all_symbols.extend(dax_symbols)

        # NASDAQ
        if option == 2:
            nasdaq100__symbols = ["RJF"]
            all_symbols.extend(nasdaq100__symbols)

        # ----------------------------------------------
        # Dax + nasdaq + excel + s&p500
        if option == 0:
            symbols52W_Hi = get52_w__h__symbols__from_excel(filepath + stock_list_name, filepath + excel_file_name)
            all_symbols.extend(symbols52W_Hi)
            all_symbols.extend(nasdaq100__symbols)
            all_symbols.extend(dax_symbols)

            option = 5  # avoid code duplication, instead of switch

        # finanzen excel
        if option == 3:
            symbols52W_Hi = get52_w__h__symbols__from_excel(filepath + stock_list_name, filepath + excel_file_name)
            all_symbols.extend(symbols52W_Hi)

        # 4 = DAX, NASDAQ , S&P500
        if option == 4:
            all_symbols.extend(nasdaq100__symbols)
            all_symbols.extend(dax_symbols)
            option = 5  # avoid code duplication, instead of switch

        # S&P500 and CDAX
        if option == 5:
            res = read_tickers(tickers_file, stocknames_file)
            all_symbols.extend(res['tickers'])
            all_names.extend(res['names'])

            #TODO wenn modified: creation_date

        # Create new threads
        splits = split_list(all_symbols, num_of_stocks_per_thread)
        stock_screening_threads = MyThread("stock_screening_threads")

        i = 0
        while i < len(splits):
            stock_names_to_check = splits[i]
            stock_screening_threads.append_thread(
                threading.Thread(target=function_for_threading_strat_scheduler,
                                 kwargs={'stock_names_to_check': stock_names_to_check, 'ago52_w_time': ago52_w,
                                         'end_l': end}))
            i += 1

        # Start new Threads to schedule all stocks
        append_to_file(
            "Start screening with " + str(len(all_symbols)) + " symbols and num_of_stocks_per_thread = " + str(
                num_of_stocks_per_thread), filepath + "Runtime.txt")
        stock_screening_threads.execute_threads()

        # print the results and plot it
        print_stocks_to_buy(stocks_to_buy, num_of_stocks_per_thread, program_start_time, datetime.now(),
                            filepath + stock_list_name, filepath + stocks_to_buy_name)
        # plot_stocks_to_buy_as_candlechart_with_volume(stocks_to_buy, ago52_w, end)

    except Exception as e:
        traceback.print_exc()

run_stock_screening()