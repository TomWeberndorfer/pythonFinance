import inspect
import traceback

from Utils.Logger_Instance import logger
from Strategies.Abstract_Strategy import Abstract_Strategy
from Utils.Abstract_SimpleMultithreading import Abstract_SimpleMultithreading
from newsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews


class SimplePatternNewsStrategy(Abstract_Strategy):
    def __init__(self, stock_data_container_list, parameter_dict):
        Abstract_Strategy.__init__(self, stock_data_container_list, parameter_dict)
        self.text_analysis = GermanTaggerAnalyseNews(self.stock_data_container_list,
                                                     self.parameter_dict['news_threshold'],
                                                     self.parameter_dict['german_tagger'])

    def _method_to_execute(self, stock_data_container):
        try:
            result = self.text_analysis.analyse_single_news(stock_data_container)
            if result is not None:
                ppd = result.positive_prob_dist()
                if ppd >= 0.5:
                    rec = "BUY"
                else:
                    rec = "SELL"
                result.update_used_strategy_and_recommendation(self.__class__.__name__, rec)
                self.result_list.append(result)
        except Exception as e:
            logger.error("For stock: " + str(stock_data_container.get_stock_name()) + ": " + str(e) + "\n" + str(
                traceback.format_exc()))

        self.update_status("SimplePatternNewsStrategy:")

    @staticmethod
    def get_required_parameters_with_default_parameters():
        strategy_parameter_dict = \
            {'SimplePatternNewsStrategy': {'news_threshold': 0.7,
                                           'german_tagger': 'C:\\temp\\nltk_german_classifier_data.pickle',
                                           'data_readers': {'TraderfoxNewsDataReader':
                                               {
                                                   'last_date_time_file': 'C:\\temp\\last_date_time.csv',
                                                   'german_tagger': 'C:\\temp\\nltk_german_classifier_data.pickle',
                                                   'reload_data': True,
                                                   'ticker_needed': False},
                                               'HistoricalDataReader':
                                                   {'weeks_delta': 52,
                                                    'data_source': 'iex',
                                                    'reload_data': True,
                                                    'ticker_needed': False}}}}
        return strategy_parameter_dict
