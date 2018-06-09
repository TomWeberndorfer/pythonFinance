import os
from datetime import datetime
from DataReading.NewsStockDataReaders.DataReaderFactory import DataReaderFactory
from Strategies.StrategyFactory import StrategyFactory
from Utils.file_utils import FileUtils, read_tickers_from_file_or_web
from Utils.news_utils import NewsUtils


def run_analysis(selected_strategies_list, strategy_parameter_dict, other_params):
    # TODO 10: only temp:
    try:
        import os
        os.remove("C:\\temp\\pythonFinance\\pythonFinance\\DataFiles\\last_date_time.csv")
    except Exception:
        pass
    reload = True

    thr_start = datetime.now()
    stock_data_container_list = read_tickers_from_file_or_web(other_params['stock_data_container_file'], reload,
                                                              other_params['list_with_stock_pages_to_read'])
    reader_results = {}
    readers = {}
    for selected_strat in selected_strategies_list:
        for data_reader in strategy_parameter_dict[selected_strat]['data_readers']:
            data_storage = DataReaderFactory()
            reader_type = data_reader[0]
            name = data_reader[1]
            date_file = other_params['last_date_time_file']
            readers[name] = data_storage.prepare(reader_type, stock_data_container_list, other_params['weeks_delta'],
                                                 other_params['stock_data_container_file'], other_params['data_source'],
                                                 reload, date_file)
            print("data_reader " + name + " initialised.\n")
            # only add, if not added by another strategy reader --> avoid duplications
            try:
                if reader_results[name] is None:
                    raise Exception
            except Exception:
                reader_results[name] = readers[name].read_data()

            print("data_reader " + name + " read data.\n")

    # selected strategies
    analysed_stocks = []
    for strategy_name in selected_strategies_list:
        strat_factory = StrategyFactory()

        try:
            all_news_text_list = reader_results['news_stock_data_reader']
        except Exception:
            all_news_text_list = None

        try:
            result_stock_data_container_list = reader_results['stock_data_reader']
        except Exception:
            result_stock_data_container_list = stock_data_container_list

        strategy = strat_factory.prepare_strategy(strategy_name, result_stock_data_container_list,
                                                  strategy_parameter_dict[strategy_name], all_news_text_list)
        strategy_result = strategy.run_strategy()
        analysed_stocks.extend(strategy_result)

    print("Runtime check at " + str(datetime.now()) + " and duration: " + str(datetime.now() - thr_start) + " seconds.")
    return analysed_stocks

    ##################################################
    # 52 w strategy

    if selected_strategies_list == "W52HighTechnicalStrategy":
        stock_screener = StrategyFactory()
        w52_hi_strat = stock_screener.prepare_strategy("W52HighTechnicalStrategy", stock_data_container_list,
                                                       strategy_parameter_dict)
        reader_results = w52_hi_strat.run_strategy()
        for data in reader_results:
            print("BUY: " + data.stock_name + ", " + data.stock_ticker)

    ##################################################
    # News strategy + 52 w auf reader_results
    elif selected_strategies_list == "SimplePatternNewsStrategy":

        # TODO auch hier parallel
        # news_data_storage = DataReaderFactory()
        ##news_stock_data_reader = news_data_storage.prepare("TraderfoxNewsDataReader", stock_data_container_list,
        # other_params['weeks_delta'], other_params['stock_data_container_file'], other_params['data_source'],
        # reload, other_params['last_date_time_file'])
        # all_news_text_list = news_stock_data_reader.read_data()
        all_news_text_list = readers['result']["news_stock_data_reader"]

        stock_screener = StrategyFactory()
        news_strategy = stock_screener.prepare_strategy("SimplePatternNewsStrategy", stock_data_container_list,
                                                        strategy_parameter_dict, all_news_text_list)
        reader_results = news_strategy.run_strategy()

        # todo 10 des stimmt garned zaum zwischen current price und was er wirklich is
        # for data in reader_results:
        #     if len(data.historical_stock_data) > 0:
        #         data.set_stock_current_prize(data.historical_stock_data.High[len(reader_results) - 1])
        #     else:
        #         print("ERROR: failed load hist data for " + data.stock_name)

        # 52 w strat------------------------------------------------------
        # TODO 10: warum nur mit reader_results --> weil mehr nichts bringt bei verknüpfung
        # TODO 10: eig nur de positiven nehmen???
        if 0:
            stock_data_reader = data_storage.prepare("HistoricalDataReader", reader_results, other_params['weeks_delta'],
                                                     other_params['stock_data_container_file'],
                                                     other_params['data_source'],
                                                     reload, other_params['last_date_time_file'])
            stock_data_reader.read_data()

            w52_hi_strat = stock_screener.prepare_strategy("W52HighTechnicalStrategy", reader_results, strategy_parameter_dict)
            reader_results = w52_hi_strat.run_strategy()

        # print result -------------------------
        res_str = NewsUtils.format_news_analysis_results(reader_results)

        if res_str is not None and len(res_str) > 0:
            print(res_str)
            # FileUtils.append_to_file(res_str, global_filepath + "Backtesting.txt")  # TODO da ghert a aktuelle abfrage fuer preis
            # TODO CommonUtils.send_stock_email(res_str, "News Trading: New news available")
        else:
            print("News analysis: no news")

        # time.sleep(60)  # check for new news after x seconds
    print("Runtime check at " + str(datetime.now()) + " and duration: " + str(datetime.now() - thr_start) + " seconds.")

    # TODO 10: dazu
    # result = calculate_stopbuy_and_stoploss(stock_data_container)

    return reader_results


if __name__ == '__main__':
    thr_start = datetime.now()
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # TODO ev in config file -->  gui load
    filepath = ROOT_DIR + '\\DataFiles\\'
    # data_source = 'iex'
    # weeks_delta = 52  # one year in the past
    selection = "SimplePatternNewsStrategy"
    news_parameter_dict = {'news_threshold': 0.7, 'german_tagger': filepath + 'nltk_german_classifier_data.pickle'}
    w52hi_parameter_dict = {'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98}
