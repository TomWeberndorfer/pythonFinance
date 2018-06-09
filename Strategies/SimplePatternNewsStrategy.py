import inspect
import sys

from Strategies.Strategy import Strategy
from Utils.common_utils import CommonUtils
from newsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews


class SimplePatternNewsStrategy(Strategy):
    def __init__(self, stock_data_container_list, parameter_dict, all_news_text_list):
        Strategy.__init__(self, stock_data_container_list, parameter_dict)
        self.text_analysis = GermanTaggerAnalyseNews(self.stock_data_container_list,
                                                     self.parameter_dict['news_threshold'],
                                                     self.parameter_dict['german_tagger'])
        self.all_news_text_list = all_news_text_list

    def run_strategy(self):
        stack = inspect.stack()
        #the_class = stack[1][0].f_locals["self"].__class__  # get the inherited class name
        #TODO anders updaten
        self.max_data_reads = len(self.all_news_text_list)
        if len(self.all_news_text_list) > 0:
            pool = CommonUtils.get_threading_pool()
            pool.map(self._method_to_execute, self.all_news_text_list)

        #print(str(the_class) + " finished.")
        return self.result_list

    def _method_to_execute(self, news_text):
        try:
            result = self.text_analysis.analyse_single_news(news_text)
            if result is not None:
                #TODO
                class_name = self.__class__.__name__
                result.append_used_strategy(class_name)
                self.result_list.append(result)
        except Exception as e:
            sys.stderr.write("Exception:  " + str(e) + "\n")

        self.update_status("SimplePatternNewsStrategy:")



