import inspect
import sys

from Strategies.Strategy import Strategy
from Utils.common_utils import CommonUtils
from newsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews


class SimplePatternNewsStrategy(Strategy):
    def __init__(self, stock_data_container_list, parameter_dict):
        Strategy.__init__(self, stock_data_container_list, parameter_dict)
        self.text_analysis = GermanTaggerAnalyseNews(self.stock_data_container_list,
                                                     self.parameter_dict['news_threshold'],
                                                     self.parameter_dict['german_tagger'])

    def run_strategy(self, all_news_text_list):
        stack = inspect.stack()
        #the_class = stack[1][0].f_locals["self"].__class__  # get the inherited class name
        #TODO anders updaten
        self.max_data_reads = len(all_news_text_list)
        if len(all_news_text_list) > 0:
            pool = CommonUtils.get_threading_pool()
            pool.map(self._method_to_execute, all_news_text_list)

        #print(str(the_class) + " finished.")
        return self.result_list

    def _method_to_execute(self, news_text):
        try:
            result = self.text_analysis.analyse_single_news(news_text)
            if result is not None:
                self.result_list.append(result)
        except Exception as e:
            sys.stderr.write("Exception:  " + str(e) + "\n")

        self.update_status("SimplePatternNewsStrategy:")



