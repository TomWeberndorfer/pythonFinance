from abc import abstractmethod


class AutomaticTradingBroker:
    @abstractmethod
    def connect(self):
        """
        Connect to broker instance
        :return: -
        """
        raise NotImplementedError("Abstractmethod")

    @abstractmethod
    def disconnect(self):
        """
        Disconnect from broker
        :return: -
        """
        raise NotImplementedError("Abstractmethod")

    @abstractmethod
    def execute_order(self, stock_ticker, order_type='LMT', action='SELL', quantity=1, limit_price=1,
                      security_type='STK', exchange='SMART', currency='USD'):
        """
        Create a contract and a order, read order id, execute the order, save the order to file.
        :param stock_ticker: stock ticker
        :param order_type: oder type , ex: LMT for limit orders
        :param action: BUY / SELL
        :param quantity: number of stocks to order
        :param limit_price: limit price to buy or sell
        :param security_type: STK for stocks
        :param exchange: echange to trade, SMART
        :param currency: USD / EUR
        :return:
        """
        raise NotImplementedError("Abstractmethod")

    @abstractmethod
    def read_orders(self):
        """
        Read the current order id from file
        :return: orders list
        """
        raise NotImplementedError("Abstractmethod")

    @abstractmethod
    def error_handler(self, msg):
        """
        Handles the capturing of error messages
        """
        raise NotImplementedError("Abstractmethod")
