import os
import pickle
import re
import pandas as pd




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

    data = pd.read_csv(file)
    test = data.set_index('url').T.to_dict('list')
    last_id = str(test[url][0])
    return last_id


def append_to_file(txt, file_with_path):
    if txt is None or file_with_path is None:
        raise NotImplementedError

    with open(file_with_path, "a") as myfile:
        myfile.write(str(txt) + "\n")
        myfile.write("")

    myfile.close()


def read_tickers_from_file(tickers_file, names_file, reload_file=False):
    """
       read the sp500 and CDAX tickers and saves it to given file
        :param names_file:
        :param reload_file: reload the tickers
        :param tickers_file: file to save the tickers
       :return: tickers
    """
    from Utils.common_utils import read_table_column_from_wikipedia
    # TODO:
    # https://de.wikipedia.org/wiki/Liste_von_Aktienindizes
    # https://de.wikipedia.org/wiki/EURO_STOXX_50#Zusammensetzung
    tickers = []
    all_names = []
    names_with_symbols = []
    stock_tickers_names = {'tickers': [], 'names': [], 'stock_exchange': []}

    if not os.path.exists(tickers_file) or not os.path.exists(names_file) or reload_file:
        # column 0 contains ticker symbols, column 1 contains security (=name)
        tickers = read_table_column_from_wikipedia('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
                                                   'wikitable sortable', 0)
        names_with_symbols = read_table_column_from_wikipedia(
            'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
            'wikitable sortable', 1)

        stock_tickers_names['tickers'] += tickers
        stock_tickers_names['names'] += names_with_symbols
        from itertools import repeat
        stock_tickers_names['stock_exchange'] += list(repeat("en", len(names_with_symbols)))

        # no tickers symbols available,  column 2 contains security (=name)
        all_names += read_table_column_from_wikipedia(
            'https://de.wikipedia.org/wiki/Liste_der_im_CDAX_gelisteten_Aktien',
            'wikitable sortable zebra', 2)

        # TODO temp disabled: wartung
        # from DataRead_Google_Yahoo import __get_symbols_from_names
        # all_exchanges = []
        # all_exchanges += list(repeat("de", len(all_names)))
        # tickers, names_with_symbols = __get_symbols_from_names (all_names, all_exchanges)
        #
        # stock_tickers_names['tickers'] += tickers
        # stock_tickers_names['names'] += names_with_symbols
        # stock_tickers_names['stock_exchange'] += list(repeat("de", len(names_with_symbols)))

        with open(tickers_file, "wb") as f:
            pickle.dump(stock_tickers_names['tickers'], f)

        with open(names_file, "wb") as f:
            pickle.dump(stock_tickers_names['names'], f)

            # TODO stock exchange speichern

    else:
        with open(tickers_file, "rb") as f:
            stock_tickers_names['tickers'] += pickle.load(f)

        with open(names_file, "rb") as f:
            stock_tickers_names['names'] += pickle.load(f)

    return stock_tickers_names