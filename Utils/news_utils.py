import hashlib


class NewsUtils:

    @staticmethod
    def format_news_analysis_results(stocks_to_buy):
        """
        TODO
        :param stocks_to_buy:
        :return:
        """
        if stocks_to_buy is not None and len(stocks_to_buy) > 0:
            str_print = ""

            if stocks_to_buy is not None and len(stocks_to_buy) > 0:
                buy_str = ""
                sell_str = ""

                for res in stocks_to_buy:
                    if res.stock_name is not None:
                        pos_class = round(res.prob_dist.prob("pos"), 2)
                        neg_class = round(res.prob_dist.prob("neg"), 2)
                        tmp_str = ""
                        tmp_str += (res.stock_name + ", ticker: " + res.stock_ticker +
                                    ", stock_exchange: " + res.stock_exchange +
                                    ", pos: " + str(pos_class) +
                                    " ,neg: " + str(neg_class) +
                                    " , current value: " + str(res.stock_current_prize) +
                                    " , target price: " + str(res.stock_target_price) +
                                    ", orig News: " + res.orignal_news) + "\n"
                        if pos_class > neg_class:
                            buy_str += "BUY: " + tmp_str
                        else:
                            sell_str += "SELL: " + tmp_str

                if len(buy_str) > 0:
                    str_print += "Stocks to BUY: \n"
                    str_print += buy_str

                if len(sell_str) > 0:
                    str_print += "\nStocks to SELL: \n"
                    str_print += sell_str

            return str_print


def generate_hash(url, content):
    """
    Generates a hash for comparison containing url and content
    :param url: page url
    :param content:  content of the page
    :return: id (hash md5)
    """
    hash_id = hashlib.md5(url.encode('utf-8') + str(content).encode('utf-8')).hexdigest()
    return hash_id
