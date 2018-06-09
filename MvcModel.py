from GUI.main_v1 import global_filepath


class MyModel:
    def __init__(self, vc):
        self.vc = vc
        self.available_strategies = []  # TODO ["SimplePatternNewsStrategy", "W52HighTechnicalStrategy"]
        # TODO verwenden
        self.program_parameter_dict = {'data_source': 'iex', 'weeks_delta': 52}
        self.all_parameter_dicts = {}
        w52hi_parameter_dict = {'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98}
        parameter_dict = {'news_threshold': 0.7,
                          'german_tagger': global_filepath + 'nltk_german_classifier_data.pickle'}
        # self.all_parameter_dicts = {'W52HighTechnicalStrategy': w52hi_parameter_dict, "SimplePatternNewsStrategy": parameter_dict}
        self.log_text = []
        self.strategy_selection_value = []
        self.result_stock_data_container_list = []
        self.is_thread_running = False

    def get_is_thread_running(self):
        return self.is_thread_running

    def set_is_thread_running(self, is_thread_running):
        self.is_thread_running = is_thread_running
        self.vc.is_thread_running_changed()

    def get_result_stock_data_container_list(self):
        return self.result_stock_data_container_list

    def clear_result_stock_data_container_list(self):
        self.result_stock_data_container_list = []
        self.vc.result_stock_data_container_list_changed()

    def extend_result_stock_data_container_list(self, stock_data_container_list):
        self.result_stock_data_container_list.extend(stock_data_container_list)
        self.vc.result_stock_data_container_list_changed()

    def set_strategy_selection_value(self, value):
        self.strategy_selection_value = value

    def get_strategy_selection_value(self):
        return self.strategy_selection_value

    # Delegates-- Model would call this on internal change
    def all_parameter_dicts_changed(self):
        self.vc.all_parameter_dicts_changed()

    # setters and getters
    def get_all_parameter_dicts(self):
        return self.all_parameter_dicts

    def add_to_all_parameter_dicts(self, items):
        for key, value in items.items():
            self.all_parameter_dicts.update({key: value})
        self.all_parameter_dicts_changed()

    def clear_all_parameter_dicts(self):
        self.all_parameter_dicts = {}
        self.all_parameter_dicts_changed()

    # Delegates-- Model would call this on internal change
    def list_changed(self):
        self.vc.available_strategies_changed()

    # setters and getters
    def getList(self):
        return self.available_strategies

    def add_to_available_strategies(self, item):
        myList = self.available_strategies
        myList.append(item)
        self.available_strategies = myList
        self.list_changed()

    def clear_list(self):
        self.available_strategies = []
        self.list_changed()

    def add_to_log(self, log_text):
        self.log_text.append(log_text)
        self.log_changed()

    def log_changed(self):
        self.vc.log_changed_delegate()

    def get_log(self):
        return self.log_text