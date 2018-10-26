import datetime
import importlib
import inspect
import smtplib
import sys
import traceback
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
# TODO from multiprocessing import Pool as ThreadPool
# https://stackoverflow.com/questions/5442910/python-multiprocessing-pool-map-for-multiple-arguments
import bs4 as bs

import requests

import Utils.Logger_Instance
from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Trial.try_candlesticks import plot_stock_as_candlechart_with_volume
from threading import Event, Thread


class CommonUtils:
    threadpool = None

    @staticmethod
    def send_stock_email(message_text, subject_text, from_addr='python.trading.framework@gmail.com',
                         to_addr='weberndorfer.thomas@gmail.com'):
        # TODO change standard address
        """
        Sends a stock email with the given message
        :param to_addr: send email to address
        :param from_addr: send mail from address
        :param message_text: message text for mail: content
        :param subject_text: mail subject text
        :return: status
        """

        if message_text is None or len(message_text) <= 0:
            raise AttributeError("arguments false")

        return CommonUtils.send_email(from_addr=from_addr,
                                      to_addr_list=[to_addr],
                                      cc_addr_list=[],
                                      subject=subject_text,
                                      message=message_text,
                                      login='python.trading.framework',
                                      password='8n6Qw8YoJe8m')

    @staticmethod
    def get_threading_pool(max_number_threads=300):
        """
        Returns a thread pool with maximum number of threads or the number of list len
        :param list_len: elements in the list --> number of threads (max limited)
        :param max_number_threads: maximum number of possible threads
        :return: thread pool object
        """

        if CommonUtils.threadpool is None:
            CommonUtils.threadpool = ThreadPool(max_number_threads)

        return CommonUtils.threadpool

    @staticmethod
    def send_email(from_addr, to_addr_list, cc_addr_list, subject, message, login, password,
                   smtpserver='smtp.gmail.com:587'):
        """
        TODO
        :param from_addr:
        :param to_addr_list:
        :param cc_addr_list:
        :param subject:
        :param message:
        :param login:
        :param password:
        :param smtpserver:
        :return:
        """
        header = 'From: %s\n' % from_addr
        header += 'To: %s\n' % ','.join(to_addr_list)
        header += 'Cc: %s\n' % ','.join(cc_addr_list)
        header += 'Subject: %s\n\n' % subject
        # message = u''.join((header, message)).encode('utf-8')
        message = (header + message).encode('latin-1', 'ignore')

        server = smtplib.SMTP(smtpserver)
        server.starttls()
        server.login(login, password)
        problems = server.sendmail(from_addr, to_addr_list, message)
        server.quit()
        return problems

    @staticmethod
    def is_date_today(date_to_check, date_time_format="%d.%m.%Y"):
        """
        Checks, if the given date is the current date (today)
        :param date_to_check: date to check in given format
        :param date_time_format: date time format to convert
        :return: True, if today
        """
        if date_to_check is None:
            raise NotImplementedError

        today_date_str = datetime.now().strftime(date_time_format)
        today_date = datetime.strptime(today_date_str, date_time_format)

        date_to_check_str = date_to_check.strftime(date_time_format)
        date_to_check_today = datetime.strptime(date_to_check_str, date_time_format)

        is_today = today_date == date_to_check_today
        return is_today

    @staticmethod
    def split_list(list_to_split, size):
        """
        Split into a sublist with given size each.
        :param list_to_split: list for split input
        :param size: size of split list
        :return: the final list of lists
        """
        if list_to_split is None or len(list_to_split) <= 0 or size is None:
            raise NotImplementedError

        list_of_lists = []
        while len(list_to_split) > size:
            pice = list_to_split[:size]
            list_of_lists.append(pice)
            list_to_split = list_to_split[size:]
        list_of_lists.append(list_to_split)
        return list_of_lists

    @staticmethod
    def get_current_class_and_function_name():
        """
        Returns the calling function name
        :return:
        :return: calling class and func name
        """

        current_func_name = lambda n=0: sys._getframe(n + 1).f_code.co_name
        # cf = current_func_name()  # name of this class itself
        cf1 = current_func_name(1)  # name of calling class
        stack = inspect.stack()
        # the_method = stack[1][0].f_code.co_name
        try:
            the_class = stack[1][0].f_locals["self"].__class__
        except Exception as e:
            return "METHOD/FUNCTION: " + str(cf1)

        return str(the_class) + ", METHOD/FUNCTION: " + str(cf1)

    @staticmethod
    def replace_wrong_stock_market(stock_name):
        if stock_name is None:
            raise NotImplementedError

        replace_pattern = [".MU", ".DE", ".SW", ".F", ".EX", ".TI", ".MI"]

        for pattern in replace_pattern:
            if pattern in stock_name:
                stock_name = stock_name.replace(pattern, "")
                stock_name = "ETR:" + stock_name
                break

        return stock_name

    @staticmethod
    def read_table_columns_from_webpage_list(page_dict):
        """
        TODO statt liste nur dict und diese methode weg und statt übergabeparameter in dict suchen
        :param page_dict:
        :return:
        """
        return CommonUtils.read_table_columns_from_webpage(page_dict['websource_address'], page_dict['find_name'],
                                                           page_dict['class_name'], page_dict['table_class'],
                                                           page_dict['ticker_column_to_read'],
                                                           page_dict['name_column_to_read'],
                                                           page_dict['stock_exchange'])

    @staticmethod
    def read_table_columns_from_webpage(websource_address, find_name, class_name, table_class, ticker_column_to_read,
                                        name_column_to_read, stock_exchange):
        """
        read the sp500 tickers and saves it to given file
        :param stock_exchange:
        :param name_column_to_read:
        :param find_name:
        :param ticker_column_to_read: 0 for sp500, 2 for cdax
        :param table_class: like 'wikitable sortable' or 'wikitable sortable zebra'
        :param websource_address: like wikepedia: 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        :return: stock data container list
        """
        resp = requests.get(websource_address)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find(find_name, {class_name: table_class})
        stock_data_container_list = []

        if table is None or len(table) <= 0:
            raise ConnectionError("Error establishing a database connection")

        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[ticker_column_to_read].text
            name = row.findAll('td')[name_column_to_read].text
            ticker = ticker.replace("\n", "")
            name = name.replace("\n", "")
            stock_data_container_list.append(StockDataContainer(name, ticker, stock_exchange))

        Utils.Logger_Instance.logger.info("Tickers from " + websource_address + " read.")
        return stock_data_container_list

    @staticmethod
    def read_table_columns_from_webpage_as_list(websource_address, find_name, class_name, table_class,
                                                ticker_column_to_read,
                                                name_column_to_read, stock_exchange):
        """
        read the sp500 tickers and saves it to given file
        :param stock_exchange:
        :param name_column_to_read:
        :param find_name:
        :param ticker_column_to_read: 0 for sp500, 2 for cdax
        :param table_class: like 'wikitable sortable' or 'wikitable sortable zebra'
        :param websource_address: like wikepedia: 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        :return: stock data container list
        """
        resp = requests.get(websource_address)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find(find_name, {class_name: table_class})
        ticker_list = []

        if table is None or len(table) <= 0:
            raise ConnectionError("Error establishing a database connection")

        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[ticker_column_to_read].text
            ticker = ticker.replace("\n", "")
            ticker_list.append(ticker)

        return ticker_list

    @staticmethod
    def read_table_column_from_webpage(websource_address, find_name, class_name, table_class, ticker_name_col):
        """
        read the sp500 tickers and saves it to given file
        :param find_name:
        :param class_name:
        :return:
        :param ticker_name_col: 0 for sp500, 2 for cdax
        :param table_class: like 'wikitable sortable' or 'wikitable sortable zebra'
        :param websource_address: like wikepedia: 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        :return: nothing
        """
        resp = requests.get(websource_address)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find(find_name, {class_name: table_class})
        tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[ticker_name_col].text
            ticker = ticker.replace("\n", "")
            tickers.append(ticker)

        return tickers

    @staticmethod
    def is_float(n):
        try:
            float_n = float(n)
        except ValueError:
            return False
        else:
            return True

    @staticmethod
    def is_int(n):
        try:
            float_n = float(n)
            int_n = int(float_n)
        except ValueError:
            return False
        else:
            return float_n == int_n

    @staticmethod
    def plot_stocks_to_buy_as_candlechart_with_volume(stocks_to_buy):
        """
        plots alist with stock _names
        :param stocks_to_buy:
        :param start_date:
        :param end_date:
        :return:
        """
        for stock in stocks_to_buy:
            try:
                stock_name = stock['get_stock_name']
                stock_data = stock['data']
                plot_stock_as_candlechart_with_volume(stock_name, stock_data)

            except Exception as e:
                Utils.logger.error("Unexpected Exception : " + str(e) + "\n" + str(traceback.format_exc()))

    @staticmethod
    def have_dicts_same_shape(d1, d2):
        """
        Check if dicts have the same shape, which means same nested structure and keys.
        :param d1: dict 1
        :param d2: dict 2
        :return: True, if shape is sanme
        """
        if isinstance(d1, dict):
            if isinstance(d2, dict):
                # then we have shapes to check
                return (d1.keys() == d2.keys() and
                        # so the keys are all the same
                        all(CommonUtils.have_dicts_same_shape(d1[k], d2[k]) for k in d1.keys()))
                # thus all values will be tested in the same way.
            else:
                return False  # d1 is a dict, but d2 isn't
        else:
            return not isinstance(d2, dict)  # if d2 is a dict, False, else True.

    @staticmethod
    def class_for_name(module_name, class_name):
        """
        Load the class from given module
        :param module_name: string with whole module name as string
        :param class_name: class name as string
        :return: the class
        """
        # load the module, will raise ImportError if module cannot be loaded
        m = importlib.import_module(module_name)
        # get the class, will raise AttributeError if class cannot be found
        c = getattr(m, class_name)
        return c

    @staticmethod
    def get_recursive_module(self, root):
        if str(self) in str(root):
            return str(self.stem)

        else:
            text = CommonUtils.get_recursive_module(self.parent, root)
            if text is '':
                return str(self.stem)
            else:
                return text + '.' + str(self.stem)

    @staticmethod
    def get_implemented_items_dict(file_path_glob, glob_path, keyword):
        """
        Get the implemented classes of the sub-directiory and return as dict with name and class.
        :param file_path_glob: os path of the current file: os.path.abspath variable
        :param glob_path: filter to look for, ex. the folders below: './*/**/**/*.py'
        :param keyword: keyword in the file name to search
        :return: dict with all implemented classes
        """
        items_dict = {}

        all_files = [file for file in list(file_path_glob.glob(glob_path))
                     if keyword.lower() in file.stem.lower()]

        for file in all_files:
            try:
                module_and_class = CommonUtils.get_recursive_module(file.parent, file_path_glob) + '.' + file.stem
                curr_class = CommonUtils.class_for_name(module_and_class, file.stem)
                items_dict.update({file.stem: curr_class})
            except ImportError as ie:
                pass
        return items_dict

    @staticmethod
    def call_repeatedly(interval, func, *args):
        """
        Call repeatedly the given function in interval time.
        :param interval:
        :param func:
        :param args:
        :return:
        """
        stopped = Event()

        def loop():
            while not stopped.wait(interval):  # the first call is in `interval` secs
                func(*args)

        Thread(target=loop).start()
        return stopped.set


def wrapper(func, *args, **kwargs):
    """
    Wrapps the function and the arguments
    :param func:
    :param args:
    :param kwargs:
    :return:
    """
    # do something before
    return func(*args, **kwargs)


def is_next_day_or_later(date_to_check_str, date_time_format_1, last_date,
                         date_time_format_2):
    """
    Check, if the current date string is newer than another date string
    :param date_to_check_str: date as string
    :param date_time_format_1: format of first string, ex:  "%Y-%m-%d %H:%M:%S.%f"
    :param last_date: other date time string
    :param date_time_format_2: format of second string, ex: "%d.%m.%Y um %H:%M"
    :return:
    """
    date_to_check = datetime.strptime(date_to_check_str, date_time_format_1)

    if isinstance(last_date, str):
        last_date = datetime.strptime(last_date, date_time_format_2)

    # compare the dates days ex. 2018-09-13 < 2018-09-14
    is_date_more_up_to_date = last_date.date() < date_to_check.date()

    return is_date_more_up_to_date
