import os
from datetime import datetime

from DataReading.NewsStockDataReaders.DataReaderFactory import DataReaderFactory
from RiskManagement.RiskModelFactory import RiskModelFactory
from Strategies.StrategyFactory import StrategyFactory
from Utils.Logger_Instance import logger


def run_analysis(selected_strategies_list, strategy_parameter_dict, other_params):
    """
    Run the analysis due to given parameters and returns the result as container list.
    :param selected_strategies_list: lit with selected strategies to execute
    :param strategy_parameter_dict: dict with strategy dependend parameters
    :param other_params: dict with needed parameters
    :return: analysed_stocks list
    """
    # TODO anders machen, ned hier importieren
    from Utils.file_utils import read_tickers_from_file_or_web

    thr_start = datetime.now()
    stock_data_container_list = read_tickers_from_file_or_web(other_params['stock_data_container_file'], other_params['reload_ticker'],
                                                              other_params['list_with_stock_pages_to_read'])
    reader_results = {}
    reader_names = {}
    readers = {}
    for selected_strat in selected_strategies_list:
        for data_reader in strategy_parameter_dict[selected_strat]['data_readers']:
            data_storage = DataReaderFactory()
            reader_type = data_reader[0]
            name = data_reader[1]
            date_file = other_params['last_date_time_file']
            readers[name] = data_storage.prepare(reader_type, stock_data_container_list, other_params['weeks_delta'],
                                                 other_params['stock_data_container_file'], other_params['data_source'],
                                                 other_params['reload_stock_data'], date_file)
            logger.info("data_reader " + name + " initialised.")
            # only add, if not added by another strategy reader --> avoid duplications
            try:
                if reader_results[name] is None:
                    raise Exception
            except Exception:
                reader_results[name] = readers[name].read_data()

            logger.info("data_reader " + name + " read data.")

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

        logger.info("Runtime check at " + str(datetime.now()) + " and duration: " + str(
            datetime.now() - thr_start) + " seconds.")

    # risk model
    # TODO mehrere risk model --> liste oder dict
    risk_model = other_params['RiskModel']
    rm_name = risk_model['Name']
    rm_parameters = risk_model['Parameters']
    rm_factory = RiskModelFactory()
    fsr = rm_factory.prepare(rm_name, analysed_stocks, rm_parameters)
    fsr.determine_risk()

    return analysed_stocks
