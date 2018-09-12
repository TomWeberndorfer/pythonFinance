import traceback

from NewsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews
from Signals.Signals import evaluate_signals
from Strategies.Abstract_Strategy import Abstract_Strategy
from Utils.GlobalVariables import *
from Utils.Logger_Instance import logger


class SimplePatternNewsStrategy(Abstract_Strategy):
    def add_signals(self, stock_data_container, analysis_parameters):
        """
        Add the text analysis signal
        :param stock_data_container:
        :param analysis_parameters:
        :return:
        """
        self.signal_list = [[self.text_analysis.analyse_single_news, stock_data_container]]

    def __init__(self, **kwargs):
        Abstract_Strategy.__init__(self, **kwargs)

        if not hasattr(self, "stock_data_container_list"):
            self.stock_data_container_list = []

        self.text_analysis = GermanTaggerAnalyseNews(self.stock_data_container_list,
                                                     self.analysis_parameters['news_threshold'],
                                                     self.analysis_parameters['german_tagger'])

    def _method_to_execute(self, stock_data_container):
        try:

            self.add_signals(stock_data_container, self.analysis_parameters)
            result = evaluate_signals(self.signal_list)

            if result is not None and result is not False:
                ppd = stock_data_container.positive_prob_dist()
                if ppd >= 0.5:
                    rec = "BUY"
                else:
                    rec = "SELL"

                stock_data_container.update_used_strategy_and_recommendation(self.__class__.__name__, rec)
                self.result_list.append(stock_data_container)
        except Exception as e:
            logger.error("For stock: " + str(stock_data_container.get_stock_name()) + ": " + str(e) + "\n" + str(
                traceback.format_exc()))

        self.update_status("SimplePatternNewsStrategy:")

    @staticmethod
    def get_required_parameters_with_default_parameters():

        data_file_path = GlobalVariables.get_data_files_path()
        strategy_parameter_dict = \
            {'SimplePatternNewsStrategy': {'news_threshold': 0.7,
                                           'german_tagger': data_file_path + 'nltk_german_classifier_data.pickle',
                                           'data_readers': {'TraderfoxNewsDataReader':
                                               {
                                                   'last_check_date_file': data_file_path + 'last_date_time.csv',
                                                   'german_tagger': data_file_path + 'nltk_german_classifier_data.pickle',
                                                   'reload_data': True,
                                                   'ticker_needed': False},
                                               'HistoricalDataReader':
                                                   {'weeks_delta': 52,
                                                    'data_source': 'iex',
                                                    'reload_data': True,
                                                    'ticker_needed': False}}}}
        return strategy_parameter_dict
