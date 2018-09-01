from Utils.ObjectWithChangedListeners import ListWithChangedListeners, DictWithChangedListeners, \
    ObjectWithChangedListeners


class MvcModel:
    def __init__(self):
        """
        Init the mvc model with with all listener lists.
        The model contains all parameters, which should be accessed directly.
        The parameters are objects of ObjectsWithChangedListeners, which have almost the
        same methods as the original object types.
        """
        self._column_list = []
        self.result_stock_data_container_list = ListWithChangedListeners()

        self.available_backtesting_analyzers_list = ListWithChangedListeners()
        self.selected_backtesting_analyzers_list = ListWithChangedListeners()

        self.available_backtesting_stocks_list = ListWithChangedListeners()
        self.selected_backtesting_stocks_list = ListWithChangedListeners()

        self.is_thread_running = ObjectWithChangedListeners(False)
        self.analysis_parameters = DictWithChangedListeners()

        self.selected_strategies_list = ListWithChangedListeners()
        self.available_strategies_list = ListWithChangedListeners()

        self.cerebro = ObjectWithChangedListeners(None)

    def get_column_list(self):
        return self._column_list

    def update_column_list(self, columns_to_add):
        """
        Adds columns to the column list, if not already there, does not add redundant entries.
        :param columns_to_add: list with columns to add
        :return: Returns True, if list is updated / a new entry is appended
        """
        is_updated = False
        for col in columns_to_add:
            if col not in self._column_list:
                self._column_list.append(col)
                self._column_list = list(dict.fromkeys(self._column_list))
                is_updated = True

        return is_updated
