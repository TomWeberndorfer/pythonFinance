import os
import _pickle as pickle
import re
import pandas as pd
import os.path

from DataReading.StockDataContainer import StockDataContainer
from Utils.common_utils import read_table_column_from_wikipedia
from itertools import repeat


class FileUtils:
    @staticmethod
    def read_tickers_from_file(stock_data_container_file, reload_file=False):
        """
            TODO
           read the sp500 and CDAX tickers and saves it to given file
            :param stock_exchange_file:
            :param names_file:
            :param reload_file: reload the tickers
            :param tickers_file: file to save the tickers
           :return: tickers
        """

        # TODO:
        # https://de.wikipedia.org/wiki/Liste_von_Aktienindizes
        # https://de.wikipedia.org/wiki/EURO_STOXX_50#Zusammensetzung

        # TODO weg wenn stockdatacontainer getestet
        # stock_tickers_names = {'tickers': [], 'names': [], 'stock_exchange': []}
        stock_data_container_list = []

        # TODO weg wenn stockdatacontainer getestet
        #if not os.path.exists(tickers_file) or reload_file \
        #        or not os.path.exists(names_file) \
        #        or not os.path.exists(stock_exchange_file):
            # column 0 contains ticker symbols, column 1 contains security (=name)

        if not os.path.exists(stock_data_container_file) or reload_file:

            tickers = read_table_column_from_wikipedia('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
                                                       'wikitable sortable', 0)
            names_with_symbols = read_table_column_from_wikipedia(
                'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
                'wikitable sortable', 1)

            #TODO weg wenn stockdatacontainer getestet
            #stock_tickers_names['tickers'] += tickers
            #stock_tickers_names['names'] += names_with_symbols
            #stock_tickers_names['stock_exchange'] += list(repeat("en", len(names_with_symbols)))

            stock_exchange = []
            stock_exchange += list(repeat("en", len(names_with_symbols)))

            for idx in range(0, len(tickers)):
                stock_data_container_list.append(StockDataContainer(tickers[idx], names_with_symbols[idx], stock_exchange[idx]))

            # ########## CDAX +++++++++++++

            from Utils.common_utils import read_table_column_from_webpage
            # names_with_symbols = read_table_column_from_webpage('http://topforeignstocks.com/stock-lists/the-list-of-listed-companies-in-germany/',
            #    'table', 'class', 'tablepress tablepress-id-1563 dataTable no-footer',  1)

            tickers = read_table_column_from_webpage(
                'http://topforeignstocks.com/stock-lists/the-list-of-listed-companies-in-germany/',
                'tbody', 'class', 'row-hover', 2)

            names_with_symbols = read_table_column_from_webpage(
                'http://topforeignstocks.com/stock-lists/the-list-of-listed-companies-in-germany/',
                'tbody', 'class', 'row-hover', 1)

            # TODO weg wenn stockdatacontainer getestet
            #stock_tickers_names['tickers'] += tickers
            #stock_tickers_names['names'] += names_with_symbols
            #stock_tickers_names['stock_exchange'] += list(repeat("de", len(names_with_symbols)))

            stock_exchange = []
            stock_exchange += list(repeat("de", len(names_with_symbols)))

            for idx in range(0, len(tickers)):
                stock_data_container_list.append(
                    StockDataContainer(tickers[idx], names_with_symbols[idx], stock_exchange[idx]))

            # TODO: b) General Standard is not included of page:
            # http://topforeignstocks.com/stock-lists/the-list-of-listed-companies-in-germany/

            # TODO temp disabled: wartung
            # TODO: http://www.boerse-online.de/index/liste/cdax
            # no tickers symbols available,  column 2 contains security (=name)
            # all_names += read_table_column_from_wikipedia(
            #    'https://de.wikipedia.org/wiki/Liste_der_im_CDAX_gelisteten_Aktien',
            #   'wikitable sortable zebra', 2)

            # from DataRead_Google_Yahoo import __get_symbols_from_names
            # all_exchanges = []
            # all_exchanges += list(repeat("de", len(all_names)))
            # tickers, names_with_symbols = __get_symbols_from_names (all_names, all_exchanges)
            # stock_tickers_names['tickers'] += tickers
            # stock_tickers_names['names'] += names_with_symbols
            # stock_tickers_names['stock_exchange'] += list(repeat("de", len(names_with_symbols)))

            # TODO weg wenn stockdatacontainer getestet
            # with open(tickers_file, "wb") as f:
            #     pickle.dump(stock_tickers_names['tickers'], f)
            #
            # with open(names_file, "wb") as f:
            #     pickle.dump(stock_tickers_names['names'], f)
            #
            # with open(stock_exchange_file, "wb") as f:
            #     pickle.dump(stock_tickers_names['stock_exchange'], f)

            with open(stock_data_container_file, "wb") as f:
                pickle.dump(stock_data_container_list, f)


        else:

            # TODO weg wenn stockdatacontainer getestet
            # with open(tickers_file, "rb") as f:
            #     stock_tickers_names['tickers'] += pickle.load(f)
            #
            # with open(names_file, "rb") as f:
            #     stock_tickers_names['names'] += pickle.load(f)
            #
            # with open(stock_exchange_file, "rb") as f:
            #     stock_tickers_names['stock_exchange'] += pickle.load(f)

            with open(stock_data_container_file, "rb") as f:
                stock_data_container_list += pickle.load(f)

        return stock_data_container_list

    @staticmethod
    def append_to_file(txt, file_with_path):
        """
        appends the given text to the file + path
        :param txt: text to append
        :param file_with_path: file name + path
        :return: none
        """
        if txt is None or file_with_path is None:
            raise NotImplementedError

        check_file_exists_or_create(file_with_path)  # no need to check, creates anyway

        with open(file_with_path, "a") as myfile:
            myfile.write(str(txt) + "\n")
            myfile.write("")

        myfile.close()

def replace_in_file(file, pattern, subst):
    """
    Replaces a pattern in a file with another substitute.
    :param file: file path + name
    :param pattern: pattern to replace
    :param subst: substitute
    :return: nothing
    """

    # Read contents from file as a single string
    file_handle = open(file, 'r')
    file_string = file_handle.read()
    file_handle.close()

    # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
    file_string = (re.sub(pattern, subst, file_string))

    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_handle = open(file, 'w')
    file_handle.write(file_string)
    file_handle.close()


def get_hash_from_file(file, url):
    """
    reads the hash from the hashfile, due to given url (dict style with url and hash)
    :param file: hash file path + name
    :param url: url for hash
    :return: returns the hash id
    """

    if check_file_exists_or_create(file):
        data = pd.read_csv(file)
        test = data.set_index('url').T.to_dict('list')

        last_id = str(0)
        try:
            last_id = str(test[url][0])
        except Exception:
            FileUtils.append_to_file(url + "," + str(0), file)

        return last_id

    else:
        FileUtils.append_to_file("url,hash", file)
        FileUtils.append_to_file(url + "," + str(0), file)
        return str(0)


def check_file_exists_or_create(file, txt=""):
    """
    Checks if the file exists and create it otherwise if not.
    :param txt: text to append in file, if empty
    :param file: filepath + name
    :return: true if it exists
    """
    if os.path.exists(file):
        return True
    else:
        print("\nFile " + file + " did not exist! Was created for you!\n\n")

        with open(file, "a") as myfile:
            if txt != "":
                myfile.write(str(txt) + "\n")
                myfile.write("")

        myfile.close()
        return False
