import os


class GlobalVariables:

    @staticmethod
    def get_root_dir():
        ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return ROOT_DIR

    @staticmethod
    def get_data_files_path():
        data_file_path = GlobalVariables.get_root_dir() + '\\DataFiles\\'
        return data_file_path

    @staticmethod
    def get_test_data_files_path():
        data_file_path = GlobalVariables.get_data_files_path() + '\\TestData\\'
        return data_file_path

    @staticmethod
    def get_last_used_parameter_file():
        """
        Get the last used parameter file configuration file
        :return: path + name of the config file
        """
        data_file_path = GlobalVariables.get_data_files_path() + "FileConfig.ini"
        return data_file_path

    @staticmethod
    def get_stock_data_labels_dict(uppercase=False):
        # real sorting: ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        # TODO vom dataprovider lesen und dann zuweisen (irgendeine aktie abfragen)
        # TODO dataprovider als übergabeparameter
        if uppercase is False:
            stock_data_labels_dict = {'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low',
                                      'Close': 'close', 'Volume': 'volume'}
        else:
            stock_data_labels_dict = {'Date': 'Date', 'Open': 'Open', 'High': 'High', 'Low': 'Low',
                                      'Close': 'Close', 'Volume': 'Volume'}
        return stock_data_labels_dict

    @staticmethod
    def get_stock_data_dtformat():
        """
        Get the stock data date time format.
        :return: date time format
        """
        return '%Y-%m-%d'

    @staticmethod
    def get_screening_states():
        return {'not_running': 0, 'single_screening': 1, 'repetitive_screening': 2, 'auto_trading': 3,
                'backtesting': 4}

    @staticmethod
    def get_broker_demo_port():
        """
        Get the demo / paper trading port for broker
        :return: port as number
        """
        return 7497

    @staticmethod
    def get_broker_real_port():
        """
        Get the REAL trading port for broker
        :return: port as number
        """
        return 7496

    @staticmethod
    def get_date_time_file_header():
        return "last_check_date"

    @staticmethod
    def get_trading_orders_file():
        return GlobalVariables.get_data_files_path() + "Orders.csv"

    @staticmethod
    def get_order_file_header():
        """
        Return the header for the orders file
        :return: headers as string
        """
        return 'datetime,stock_ticker,order_id,order_type,action,quantity,limit_price,security_type,exchange,currency'

    @staticmethod
    def get_other_parameters_with_default_parameters():
        """
        Return a dict with required other parameters and default parameter values.
        :return: dict with required values and default parameters
        """

        # TODO insert:
        # ['http://topforeignstocks.com/stock-lists/the-list-of-listed-companies-in-germany/',
        # 'tbody', 'class', 'row-hover', 2, 1, 'de']]

        stock_data_file = GlobalVariables.get_data_files_path() + "stock_data_container_file.pickle"
        other_parameters_dict = {'stock_data_container_file': stock_data_file,
                                 'dict_with_stock_pages_to_read': {
                                     'SP500': {
                                         'websource_address': "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                                         'find_name': 'table', 'class_name': 'class',
                                         'table_class': 'wikitable sortable',
                                         'ticker_column_to_read': 0, 'name_column_to_read': 1, 'stock_exchange': 'en'},
                                     'DAX': {
                                         'websource_address': "http://topforeignstocks.com/stock-lists/the-list-of-listed-companies-in-germany/",
                                         'find_name': 'tbody', 'class_name': 'class', 'table_class': 'row-hover',
                                         'ticker_column_to_read': 2, 'name_column_to_read': 1, 'stock_exchange': 'de'}},
                                 'RiskModels': {
                                     'FixedSizeRiskModel': {'OrderTarget': 'order_target_value', 'TargetValue': 2500}},
                                 'AutoTrading': {
                                     'RepetitiveScreeningInterval': 120,
                                     'MaxNumberOfDifferentStocksToBuyPerAutoTrade': 5},
                                 'Broker': {
                                     'Name': 'IBPyInteractiveBrokers'}
                                 }
        return other_parameters_dict

    @staticmethod
    def get_backtesting_parameters_with_default_parameters():
        """
        Return a dict with required backtesting parameters and default parameter values.
        :return: dict with required values and default parameters
        :key trade_commission_percent: Trading commission for both orders in percent of order in percent, both, not for every trade!
        :key initial_cash: Initial cash to trade with.
        """
        backtesting_parameters = {'BacktestingFramework': 'BacktraderWrapper', 'initial_cash': 30000,
                                  'trade_commission_percent': 0.01}
        parameters_dict = {"BacktestingParameters": backtesting_parameters}

        return parameters_dict

    @staticmethod
    def get_row_colors():
        """
        Returns a dict with positive and negative colors for the tree view rows
        'PositiveColor': color for positive entries in tree view
        'NegativeColor': color for negative entries in tree view
        :return: dict with colors
        """
        return {'PositiveColor': 'lightgreen', 'NegativeColor': 'salmon'}
