from MyThread import MyThread
from Strategies.Strategy import Strategy
from newsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews


class SimplePatternNewsStrategy(Strategy, MyThread):
    def __init__(self, stock_data_container_list, parameter_dict):
        Strategy.__init__(self, parameter_dict['num_of_stocks_per_thread'], stock_data_container_list, parameter_dict)
        MyThread.__init__(self, parameter_dict['num_of_stocks_per_thread'])
        self.text_analysis = GermanTaggerAnalyseNews(self.stock_data_container_list,
                                                     self.parameter_dict['news_threshold'],
                                                     self.parameter_dict['german_tagger'])

    def run_strategy(self, all_news_text_list):
        self._append_list(all_news_text_list)
        self._execute_threads()

        return self.result_list

    def _method_to_execute(self, stock_data_container_sub_list):
        # TODO bezeichnung stock_data_container_sub_list is falsch --> news sub list
        for single_news_text in stock_data_container_sub_list:
            self.result_list.append(self.text_analysis.analyse_single_news(single_news_text))
