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
