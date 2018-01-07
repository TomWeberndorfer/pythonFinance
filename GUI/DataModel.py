class Observable:
    def __init__(self, initialValue=None):
        self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

    def _docallbacks(self):
        for func in self.callbacks:
            func(self.data)

    def set(self, data):
        self.data = data
        self._docallbacks()

    def get(self):
        return self.data

    def unset(self):
        self.data = None


class StrategyAndParameter:
    def __init__(self):
        self.selected_strategy_type = ""  # string with name of call function
        self.strategy_parameters = []  # list with parameters, e.g.:{'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98}
        self.available_strategy_types = []  # list with available types

    def set_strategy_type(self, strategy_type):
        self.selected_strategy_type = strategy_type

    def set_available_strategy_types(self, strategy_types):
        self.available_strategy_types = strategy_types

    def set_strategy_parameters(self, strategy_parameters):
        self.strategy_parameters = strategy_parameters


class StockFilter:
    def __init__(self):
        self.available_stock_indices = Observable(["CDAX", "SP500", "Test1"]) #TODO # list with stock indices (DAX,..)
        self.selected_index = Observable("")

    def set_available_stock_indices(self, available_stock_indices):
        self.available_stock_indices = available_stock_indices

    def set_selected_index(self, selected_index):
        self.selected_index = selected_index


class StockResults:
    def __init__(self):
        self.stocks_to_buy = []  # list with stocks
        self.logging_line = ""

    def append_stock(self, stock):
        self.stocks_to_buy.append(stock)


class StockData:
    def __init__(self):
        self.stocks_name = ""
        self.stock_price_data = []
        self.stock_news_data = []
    # 'stock_name': res['stock_name'], 'sb': res['sb'], 'sl': res['sl'], 'strategy_name': res['strategy_name'], 'params': params[0], 'data': stock52_w})


class OrderManagement:
    def __init__(self):
        self.stop_loss = 0
        self.stop_buy = 0
        self.strategy_parameters = []


class DataModel:
    #TODO des is eig des vom filter
    def __init__(self):
        self.available_stock_indices = Observable(["CDAX", "SP500", "Test1"]) #TODO # list with stock indices (DAX,..)
        self.selected_index = Observable("")

    def set_available_stock_indices(self, available_stock_indices):
        self.available_stock_indices = available_stock_indices

    def set_selected_index(self, selected_index):
        self.selected_index = selected_index
