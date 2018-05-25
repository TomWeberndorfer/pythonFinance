from Strategies.Strategy import Strategy
from Utils.common_utils import create_threading_pool
from newsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews
from multiprocessing.dummy import Pool as ThreadPool


class SimplePatternNewsStrategy(Strategy, ):
    def __init__(self, stock_data_container_list, parameter_dict):
        Strategy.__init__(self, parameter_dict['num_of_stocks_per_thread'], stock_data_container_list, parameter_dict)
        self.text_analysis = GermanTaggerAnalyseNews(self.stock_data_container_list,
                                                     self.parameter_dict['news_threshold'],
                                                     self.parameter_dict['german_tagger'])

    def run_strategy(self, all_news_text_list):
        pool = create_threading_pool(len(all_news_text_list))
        pool.map(self._method_to_execute, all_news_text_list)
        return self.result_list

    def _method_to_execute(self, news_text):
        self.result_list.append(self.text_analysis.analyse_single_news(news_text))
