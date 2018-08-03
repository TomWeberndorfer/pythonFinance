import os
from datetime import datetime
import _pickle as pickle
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
    stock_data_container_list = []
    thr_start = datetime.now()

    stock_data_container_list = _read_data(selected_strategies_list, strategy_parameter_dict, other_params,
                                           stock_data_container_list)

    # selected strategies

    analysed_stocks = []
    for strategy_name in selected_strategies_list:
        strat_factory = StrategyFactory()
        result_stock_data_container_list = stock_data_container_list

        strategy = strat_factory.prepare_strategy(strategy_name, result_stock_data_container_list,
                                                  strategy_parameter_dict[strategy_name])
        strategy_result = strategy.run_strategy()
        analysed_stocks.extend(strategy_result)

    # risk model
    # TODO mehrere risk model --> liste oder dict
    risk_model = other_params['RiskModel']
    rm_name = risk_model['Name']
    rm_parameters = risk_model['Parameters']
    rm_factory = RiskModelFactory()
    fsr = rm_factory.prepare(rm_name, analysed_stocks, rm_parameters)
    fsr.determine_risk()

    logger.info("Runtime at " + str(datetime.now()) + " for run analysis and duration: " + str(
        datetime.now() - thr_start) + " seconds.")

    return analysed_stocks


def _read_data(selected_strategies_list, strategy_parameter_dict, other_params, stock_data_container_list):
    reader_results = {}
    readers = {}
    for selected_strat in selected_strategies_list:
        for data_reader_params in strategy_parameter_dict[selected_strat]['data_readers']:
            data_storage = DataReaderFactory()
            reader_type = data_reader_params['Name']

            # TODO anders machen, ned hier importieren
            from Utils.file_utils import read_tickers_from_web, read_tickers_and_data_from_file
            if data_reader_params['ticker_needed']:
                if data_reader_params['reload_data'] is True:
                    stock_data_container_list = read_tickers_from_web(other_params['stock_data_container_file'],
                                                                      other_params['list_with_stock_pages_to_read'])
                else:
                    stock_data_container_list = read_tickers_and_data_from_file(
                        other_params['stock_data_container_file'])

            readers[reader_type] = data_storage.prepare(reader_type, stock_data_container_list,
                                                        data_reader_params['reload_data'],
                                                        data_reader_params)
            logger.info("data_reader " + reader_type + " initialised.")
            # only add, if not added by another strategy reader --> avoid duplications
            try:
                if reader_results[reader_type] is None:
                    raise Exception
            except Exception:
                reader_results[reader_type] = 'Read'
                # TODO stock_data_container_list.extend(readers[reader_type].read_data())
                readers[reader_type].read_data()

    # dump for next run, instead of reloading every time
    with open(other_params['stock_data_container_file'], "wb") as f:
        pickle.dump(stock_data_container_list, f)

    logger.info("data_reader " + reader_type + " read data.")

    return stock_data_container_list
