import os.path
import re
import traceback
import _pickle as pickle
import pandas as pd

from Utils.CommonUtils import CommonUtils
from Utils.Logger_Instance import logger


class FileUtils:

    @staticmethod
    def append_textline_to_file(text, file_with_path, insert_only_new_content=False):
        """
        appends the given text to the file + path
        :param insert_only_new_content: only insert the text, if it is not already in there
        :param text: text to append
        :param file_with_path: file name + path
        :return: True, if line not already in file
        """
        if text is None or file_with_path is None:
            raise NotImplementedError

        FileUtils.check_file_exists_or_create(file_with_path)  # no need to check, creates anyway

        if insert_only_new_content:
            with open(file_with_path, 'r') as myfile:
                file_content = myfile.read()
                if str(text) in file_content:
                    myfile.close()
                    return False

        with open(file_with_path, "a") as myfile:
            myfile.write(str(text) + "\n")

        myfile.close()

        return True

    @staticmethod
    def append_text_list_to_file(text_list, file_with_path, insert_only_new_content=False, separator="\n"):
        """
        appends the given text to the file + path
        :param insert_only_new_content: only insert the text, if it is not already in there
        :param text_list: list with text to append
        :param file_with_path: file name + path
        :param separator: separator between to text entries
        :return: True, if at least one line not already in file
        """
        if text_list is None or file_with_path is None:
            raise NotImplementedError

        FileUtils.check_file_exists_or_create(file_with_path)  # no need to check, creates anyway
        new_content = False
        text_to_append = []

        if insert_only_new_content:
            with open(file_with_path, 'r') as myfile:
                file_content = myfile.read()
                for text in text_list:
                    if str(text) in file_content:
                        pass
                    else:
                        text_to_append.append(str(text))
                        new_content = True
        else:
            text_to_append = text_list
            new_content = True

        with open(file_with_path, "a") as myfile:
            for text in text_to_append:
                if text_to_append.index(text) == len(text_to_append) - 1:
                    myfile.write(str(text) + "\n")
                else:
                    myfile.write(str(text) + separator)
        return new_content

    @staticmethod
    def read_tickers_and_data_from_file(stock_data_container_file):
        """
        Read the pickle file with stock data container for tickers and data.
        :param stock_data_container_file: pickle data file
        :return: container list
        """
        stock_data_container_list = []

        if ".pickle" in stock_data_container_file:
            if os.path.exists(stock_data_container_file):
                logger.info("Start reading tickers from file...")

                with open(stock_data_container_file, "rb") as f:
                    stock_data_container_list += pickle.load(f)
        else:
            logger.error("Please select a *.pickle file for the stock_data_container_file!")

        return stock_data_container_list

    @staticmethod
    def read_tickers_from_web(stock_data_container_file, list_with_stock_pages_to_read=[]):
        """
           Read the gives list of stock pages
            :param list_with_stock_pages_to_read:
            :param stock_data_container_file:
           :return: stock_data_container_list
        """

        stock_data_container_list = []
        logger.info("Start reading tickers from web...")

        pool = CommonUtils.get_threading_pool()
        result_list = pool.map(CommonUtils.read_table_columns_from_webpage_list, list_with_stock_pages_to_read)

        for result in result_list:
            stock_data_container_list.extend(result)

        with open(stock_data_container_file, "wb") as f:
            pickle.dump(stock_data_container_list, f)

        return stock_data_container_list

    @staticmethod
    def read_tickers_from_file_or_web(stock_data_container_file, reload_file=False, list_with_stock_pages_to_read=[]):
        """
            TODO
           read the sp500 and CDAX tickers and saves it to given file
            :param list_with_stock_pages_to_read:
            :param stock_data_container_file:
            :param stock_exchange_file:
            :param names_file:
            :param reload_file: reload the tickers
            :param tickers_file: file to save the tickers
           :return: stock_data_container_list
        """

        # TODO:
        # https://de.wikipedia.org/wiki/Liste_von_Aktienindizes
        # https://de.wikipedia.org/wiki/EURO_STOXX_50#Zusammensetzung

        stock_data_container_list = []

        if not os.path.exists(stock_data_container_file) or reload_file:
            logger.info("Start reading tickers...")

            pool = CommonUtils.get_threading_pool()
            result_list = pool.map(CommonUtils.read_table_columns_from_webpage_list, list_with_stock_pages_to_read)

            for result in result_list:
                stock_data_container_list.extend(result)

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
            # stock_tickers_names['_names'] += names_with_symbols
            # stock_tickers_names['_stock_exchange'] += list(repeat("de", len(names_with_symbols)))

            with open(stock_data_container_file, "wb") as f:
                pickle.dump(stock_data_container_list, f)

        else:
            with open(stock_data_container_file, "rb") as f:
                stock_data_container_list += pickle.load(f)

        return stock_data_container_list

    @staticmethod
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

    @staticmethod
    def get_hash_from_file(file, url):
        """
        reads the hash from the hashfile, due to given url (dict style with url and hash)
        :param file: hash file path + name
        :param url: url for hash
        :return: returns the hash id
        """

        if FileUtils.check_file_exists_or_create(file):
            data = pd.read_csv(file)
            test = data.set_index('url').T.to_dict('list')

            last_id = str(0)
            try:
                last_id = str(test[url][0])
            except Exception:
                FileUtils.append_textline_to_file(url + "," + str(0), file)

            return last_id

        else:
            FileUtils.append_textline_to_file("url,hash", file)
            FileUtils.append_textline_to_file(url + "," + str(0), file)
            return str(0)

    @staticmethod
    def check_file_exists_or_create(file, txt=""):
        """
        Checks if the file exists and create it otherwise if not.
        :param txt: text to append in file, if empty
        :param file: GlobalVariables.get_data_files_path() + name
        :return: true if it exists
        """
        if os.path.exists(file):
            return True
        else:
            logger.info("\nFile " + file + " did not exist! Was created for you!")

            with open(file, "a") as myfile:
                if txt != "":
                    myfile.write(str(txt) + "\n")
                    myfile.write("")

            myfile.close()
            return False

    @staticmethod
    def check_file_exists_and_delete(filename):
        """
        Check, if file exists and deletes it.
        :param filename: file name + path
        :return: -
        """
        if os.path.isfile(filename):
            os.remove(filename)
        else:  ## Show an error ##
            logger.info("File not found: " + str(filename))
