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
        #real sorting: ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
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
        return {'not_running': 0, 'single_screening': 1, 'repetititve_screening': 2, 'auto_trading': 3,
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
