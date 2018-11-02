from datetime import datetime
import _pickle as pickle
from DataReading.DataReaderFactory import DataReaderFactory
from RiskManagement.RiskModelFactory import RiskModelFactory
from Strategies.StrategyFactory import StrategyFactory
from Utils.Logger_Instance import logger


def run_analysis(selected_strategies_list, strategy_parameter_dict, other_params, stock_data_container_list=[]):
    """
    Run the analysis due to given parameters and returns the result as container list.
    :param selected_strategies_list: lit with selected strategies to execute
    :param strategy_parameter_dict: dict with strategy dependend parameters
    :param other_params: dict with needed parameters
    :return: analysed_stocks list
    """
    thr_start = datetime.now()

    if len(stock_data_container_list) <= 0:
        stock_data_container_list = []
        stock_data_container_list = _read_data(selected_strategies_list, strategy_parameter_dict, other_params,
                                               stock_data_container_list)

    # selected strategies
    # todo News + 52 w geht schon wieda ned gleichzeitig
    analysed_stocks = []
    for strategy_name in selected_strategies_list:
        strat_factory = StrategyFactory()
        result_stock_data_container_list = stock_data_container_list

        strategy = strat_factory.prepare(strategy_name,
                                         stock_data_container_list=result_stock_data_container_list,
                                         analysis_parameters=strategy_parameter_dict[strategy_name])
        strategy_result = strategy.run_strategy()
        analysed_stocks.extend(strategy_result)

    # risk model
    risk_models = other_params['RiskModels']
    for rm_name in risk_models.keys():
        rm_parameters = risk_models[rm_name]
        rm_factory = RiskModelFactory()
        fsr = rm_factory.prepare(rm_name, stock_data_container_list=analysed_stocks, parameter_dict=rm_parameters)
        fsr.determine_risk()

    logger.info("Runtime at " + str(datetime.now()) + " for run analysis and duration: " + str(
        datetime.now() - thr_start) + " seconds.")

    return analysed_stocks


def _read_data(selected_strategies_list, strategy_parameter_dict, other_params, stock_data_container_list):
    reader_results = {}
    for selected_strat in selected_strategies_list:
        for data_reader in strategy_parameter_dict[selected_strat]['data_readers']:
            data_reader_params = strategy_parameter_dict[selected_strat]['data_readers'][data_reader]
            data_storage = DataReaderFactory()
            reader_type = data_reader

            # TODO anders machen, ned hier importieren
            from Utils.FileUtils import FileUtils
            if data_reader_params['ticker_needed']:
                if data_reader_params['reload_data'] is True:
                    stock_data_container_list.extend(FileUtils.read_tickers_from_web(
                        other_params['stock_data_container_file'],
                        other_params['dict_with_stock_pages_to_read']))
                else:
                    try:
                        stock_data_container_list.extend(FileUtils.read_tickers_and_data_from_file(
                            other_params['stock_data_container_file']))
                    except RecursionError as e:
                        raise RecursionError("Reload the data, old data is maybe faulty")

            curr_reader = data_storage.prepare(reader_type,
                                               stock_data_container_list=stock_data_container_list,
                                               reload_stockdata=data_reader_params['reload_data'],
                                               parameter_dict=data_reader_params)
            logger.info("data_reader " + reader_type + " initialised.")
            # only add, if not added by another strategy reader --> avoid duplications
            # try:
            #     if reader_results[reader_type] is None:
            #         raise Exception
            # except Exception:
            # reader_results[reader_type] = 'Read'
                # TODO stock_data_container_list.extend(readers[reader_type].read_data())
            curr_reader.read_data()

    # dump for next run, instead of reloading every time
    with open(other_params['stock_data_container_file'], "wb") as f:
        pickle.dump(stock_data_container_list, f)

    logger.info("data_reader " + reader_type + " read data.")

    return stock_data_container_list
