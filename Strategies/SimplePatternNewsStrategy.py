import inspect
import sys

from Strategies.Abstract_Strategy import Abstract_Strategy
from Utils.Abstract_SimpleMultithreading import Abstract_SimpleMultithreading
from Utils.common_utils import CommonUtils, get_current_function_name
from newsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews


class SimplePatternNewsStrategy(Abstract_Strategy, Abstract_SimpleMultithreading):
    def __init__(self, stock_data_container_list, parameter_dict, all_news_text_list):
        Abstract_Strategy.__init__(self, stock_data_container_list, parameter_dict)
        Abstract_SimpleMultithreading.__init__(self)
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
            self.map_list(self.all_news_text_list)

        #print(str(the_class) + " finished.")
        return self.result_list

    def _method_to_execute(self, news_text):
        try:
            result = self.text_analysis.analyse_single_news(news_text)
            if result is not None:
               result.append_used_strategy(self.__class__.__name__)
               self.result_list.append(result)
        except Exception as e:
            sys.stderr.write("Exception in " + str(get_current_function_name()) + ":" + str(e) + "\n"+ ", news_text: " + str(news_text))

        self.update_status("SimplePatternNewsStrategy:")



