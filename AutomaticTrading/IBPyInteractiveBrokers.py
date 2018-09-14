import traceback

from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection
import pandas as pd
from Utils.FileUtils import FileUtils
from Utils.GlobalVariables import GlobalVariables
from datetime import datetime
from Utils.Logger_Instance import logger

# they are "error codes" but this is just info
info_codes = [2104, 2106]


class IBPyInteractiveBrokers:
    def __init__(self):
        # Connect to the Trader Workstation (TWS) running on the
        # usual port of 7496, with a clientId of 100
        # (The clientId is chosen by us and we will need
        # separate IDs for both the execution connection and
        # market data connection)
        self.tws_conn = Connection.create(port=GlobalVariables.get_broker_demo_port(), clientId=999)
        self.error_message_list = []

    def connect(self):
        self.tws_conn.connect()

        # Assign the error handling function defined above
        # to the TWS connection
        self.tws_conn.register(self.error_handler, 'Error')

        # Assign all of the server reply messages to the
        # reply_handler function defined above
        self.tws_conn.registerAll(self.reply_handler)

    def disconnect(self):
        # Disconnect from TWS
        self.tws_conn.disconnect()

    def get_and_clear_error_message_list(self):
        """
        Get the error message list, replied by the server and delete clera it then.
        :return: error message list from server
        """
        err_msg_list = self.error_message_list.copy()
        self.error_message_list = []
        return err_msg_list

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

        # Create a contract  via SMART order routing
        current_contract = self.create_contract(stock_ticker, security_type, exchange, exchange, currency)
        current_order = self.create_order(order_type, quantity, action, limit_price)

        # Use the connection to the send the order to IB
        order_id = self._read_current_order_id()
        try:
            self.tws_conn.placeOrder(int(order_id), current_contract, current_order)
            text_line = str(datetime.now()) + "," + str(stock_ticker) + "," + str(order_id) + "," + str(
                order_type) + "," + str(action) + "," + str(quantity) + "," + str(limit_price) + "," + str(
                security_type) + "," + str(exchange) + "," + str(currency)
            logger.info("***************************************")
            logger.info("Order was placed: " + text_line)
            logger.info("***************************************")
        except Exception as e:
            logger.error("Unexpected Exception : " + str(e) + "\n" + str(traceback.format_exc()))

        self._save_current_order(order_id, stock_ticker, GlobalVariables.get_trading_orders_file(), order_type, action,
                                 quantity,
                                 limit_price, security_type, exchange, currency)

    def _save_current_order(self, order_id, stock_ticker,
                            file_path=GlobalVariables.get_trading_orders_file(), order_type='', action='', quantity=0,
                            limit_price=0, security_type='STK', exchange='SMART', currency='USD'):
        """
        Save the current order into file.
        :param order_id: order id by interactive broker, must be unique
        :param stock_ticker: stock ticker
        :param file_path: filename + path
        :param order_type: oder type , ex: LMT for limit orders
        :param action: BUY / SELL
        :param quantity: number of stocks to order
        :param limit_price: limit price to buy or sell
        :param security_type: STK for stocks
        :param exchange: echange to trade, SMART
        :param currency: USD / EUR
        :return: nothing
        """
        FileUtils.check_file_exists_or_create(file_path, GlobalVariables.get_order_file_header())

        text_line = str(datetime.now()) + "," + str(stock_ticker) + "," + str(order_id) + "," + str(
            order_type) + "," + str(action) + "," + str(quantity) + "," + str(limit_price) + "," + str(
            security_type) + "," + str(exchange) + "," + str(currency)
        FileUtils.append_textline_to_file(text_line, file_path, False)

    def _read_current_order_id(self, file_path=GlobalVariables.get_trading_orders_file()):
        """
        Read the current order id from file
        :param file_path: filename and path
        :return: order id
        """

        # Create an order ID which is 'global' for this session. This
        # will need incrementing once new orders are submitted.
        last_order_id = pd.np.random.randint(1000, 90000)

        if FileUtils.check_file_exists_or_create(file_path, GlobalVariables.get_order_file_header()):
            data = pd.read_csv(file_path)

            if len(data) > 0:
                last_order_id = data['order_id'][len(data) - 1]

        order_id = last_order_id + 1
        return order_id

    def read_orders(self, file_path=GlobalVariables.get_trading_orders_file()):
        """
        Read the current order id from file
        :param file_path: filename and path
        :return: order id
        """
        orders = []
        # Create an order ID which is 'global' for this session. This
        # will need incrementing once new orders are submitted.
        if FileUtils.check_file_exists_or_create(file_path, GlobalVariables.get_order_file_header()):
            data = pd.read_csv(file_path)

            if len(data) > 0:
                # datetime, stock_ticker
                orders = data

        return orders

    def error_handler(self, msg):
        """Handles the capturing of error messages"""
        print("Server Error: %s" % msg)

        if msg.errorCode not in info_codes:  # this is just a ping
            logger.error("Unexpected Exception : %s" % msg)

    def reply_handler(self, msg):
        """Handles of server replies"""
        print("Server Response: %s, %s" % (msg.typeName, msg))
        logger.info("Server Response: %s, %s" % (msg.typeName, msg))

    def create_contract(self, symbol, sec_type, exch, prim_exch, curr):
        """Create a Contract object defining what will
        be purchased, at which exchange and in which currency.
        symbol - The ticker symbol for the contract
        sec_type - The security type for the contract ('STK' is 'stock')
        exch - The exchange to carry out the contract on
        prim_exch - The primary exchange to carry out the contract on
        curr - The currency in which to purchase the contract"""
        contract = Contract()
        contract.m_symbol = symbol
        contract.m_secType = sec_type
        contract.m_exchange = exch
        contract.m_primaryExch = prim_exch
        contract.m_currency = curr
        return contract

    def create_order(self, order_type, quantity, action, lmtPrice):
        """Create an Order object (Market/Limit) to go long/short.
        order_type - 'MKT', 'LMT' for Market or Limit orders
        quantity - Integral number of assets to order
        action - 'BUY' or 'SELL'"""
        order = Order()
        order.m_orderType = order_type
        order.m_totalQuantity = quantity
        order.m_action = action

        if order_type is 'LMT':
            order.m_lmtPrice = lmtPrice

        return order
