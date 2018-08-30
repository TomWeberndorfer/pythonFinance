#! /usr/bin/env python
#
# Support module generated by PAGE version 4.9
# In conjunction with Tcl version 8.6
#    Jun 03, 2018 10:50:55 AM
import _pickle as pickle
from os.path import basename
import queue
import tkinter as tk
import traceback
from threading import Thread
from tkinter import messagebox
import logging
from Utils.Logger_Instance import logger
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Labelframe
import backtrader as bt
from Backtesting.BacktraderWrapper import BacktraderWrapper
from GUI.ScrollableFrame import ScrollableFrame
from Strategies.StrategyFactory import StrategyFactory
from MvcModel import MvcModel
from StockAnalysis import run_analysis
from tkinter import *
import webbrowser as wb
import datetime  # For datetime objects
from tkinter import filedialog
import backtrader.feeds as btfeeds
import backtrader.analyzers as btanalyzer
from Utils.GlobalVariables import *
from Utils.GuiUtils import GuiUtils, evaluate_list_box_selection, set_buttons_state
from Utils.common_utils import have_dicts_same_shape, get_current_class_and_function_name
from Utils.file_utils import FileUtils
import ast
import configparser


class MyController:
    """
    Classs for the controlling of mvc design with gui
    """

    def __init__(self, parent, view):
        self.parent = parent
        self.model = MvcModel()  # initializes the model
        self.view = view  # initializes the view
        self.view.ButtonRunStrategy.config(command=self.start_screening)
        self.view.Scrolledlistbox_selectStrategy.bind('<<ListboxSelect>>', self.listbox_onselect_select_strategy)
        self.view.sl_bt_select_stocks.bind('<<ListboxSelect>>', self.listbox_onselect_select_backtesting_stocks)
        self.view.sb_select_analyzers.bind('<<ListboxSelect>>', self.listbox_onselect_select_backtesting_analyzers)
        self.view.Scrolledtreeview1.bind("<Double-1>", self.on_double_click_Scrolledtreeview1)
        self.view.b_run_backtest.config(command=self.start_backtesting)

        self.view.b_open_results_new_wd.config(command=self.plot_backtesting)

        self.analysis_parameters_changed()
        init_result_table(self.view.Scrolledtreeview1, self.model.get_column_list())
        self.console = ConsoleUi(self.view.Labelframe2)

        # add the listeners to mvc model
        # self.model.selected_backtesting_analyzers_list.add_event_listeners()
        self.model.available_backtesting_analyzers_list.add_event_listeners(self.backtesting_analyzers_list_changed)

        # TODO load from file: analyzers
        analyzer_list = [btanalyzer.AnnualReturn, btanalyzer.Calmar, btanalyzer.DrawDown, btanalyzer.TimeDrawDown,
                         btanalyzer.GrossLeverage, btanalyzer.PositionsValue, btanalyzer.Returns,
                         btanalyzer.SharpeRatio, btanalyzer.TradeAnalyzer]

        for analyzer in analyzer_list:
            self.model.available_backtesting_analyzers_list.append(analyzer)

        self.model.available_backtesting_stocks_list.add_event_listeners(self.backtesting_stocks_list_changed)

        # no need to add event lister
        # self.model.selected_strategies_list.add_event_listeners(self.strategy_selection_changed)
        self.model.available_strategies_list.add_event_listeners(self.available_strategies_changed)

        self.model.result_stock_data_container_list.add_event_listeners(self.result_stock_data_container_list_changed)
        self.model.is_thread_running.add_event_listeners(self.is_thread_running_changed)
        self.model.analysis_parameters.add_event_listeners(self.analysis_parameters_changed)
        self.model.cerebro.add_event_listeners(self.cerebro_result_changed)

        self.current_parameterfile = ""

    def on_double_click_Scrolledtreeview1(self, event):
        """
        On double click event for scrolledtreeview1,
        opens a finance web page
        :param event:
        :return:
        """
        try:
            cur_selection = self.view.Scrolledtreeview1.selection()[0]
            cur_stock = self.view.Scrolledtreeview1.item(cur_selection)

            # TODO je nachj container unterschiedlich 2 --> name is first
            # TODO einstellen der aufruf seite
            stock_name = cur_stock['values'][2]
            url_to_open = "http://www.finanzen.at/suchergebnisse?_type=Aktien&_search="
            wb.open_new_tab(url_to_open + stock_name)
        except IndexError as e:
            pass  # nothing to do for index error (may clicked at header)
        except Exception as e:
            logger.error("Exception while opening result stock: " + str(e) + "\n" + str(traceback.format_exc()))

    def start_screening(self):
        """
        Start the screening thread for NON blocking GUI.
        :return: nothing
        """
        if not self.model.is_thread_running.get():
            thread = Thread(target=self.screening)
            thread.start()

    def start_backtesting(self):
        """
        Start the backtesting thread for NON blocking GUI.
        :return: nothing
        """
        if not self.model.is_thread_running.get():
            thread = Thread(target=self.backtesting)
            thread.start()

    def screening(self):
        """
        Method to start the screening once, should be executed in a THREAD.
        :return: nothing, results are saved in the model.
        """
        try:
            selection_values = self.model.selected_strategies_list.get()

            if selection_values == "" or len(selection_values) <= 0:
                messagebox.showerror("Selection Error", "Please select a strategy first!")
                return

            req_params = StrategyFactory.get_required_parameters_with_default_parameters()
            at_objects = w.scrollable_frame_parameters.form.at_objects
            content_others = w.scrollable_frame_parameters.form.get_parameters(at_objects)

            if not self.accept_parameters_from_text(content_others, req_params):
                messagebox.showerror("Parameter file is not valid!",
                                     "Please choose a valid parameters file!")

            self.model.is_thread_running.set(True)
            logger.info("Screening started...")
            self.model.result_stock_data_container_list.clear()
            analysis_params = self.model.analysis_parameters.get()
            results = run_analysis(selection_values, analysis_params['Strategies'], analysis_params['OtherParameters'])

            self.model.result_stock_data_container_list.extend(results)
        except Exception as e:
            logger.error("Exception while screening: " + str(e) + "\n" + str(traceback.format_exc()))

        self.model.is_thread_running.set(False)

    def backtesting(self):
        """
        Method to start the backtesting once, should be executed in a THREAD.
        :return: nothing, results are saved in the model.
        """
        try:
            strategy_selections = self.model.selected_strategies_list.get()
            selected_backtesting_analyzers_str = self.model.selected_backtesting_analyzers_list.get()
            selected_backtesting_stocks = self.model.selected_backtesting_stocks_list.get()

            if strategy_selections == "" or not len(strategy_selections) is 1:
                messagebox.showerror("Selection Error", "Please select exactly ONE strategie to run in backtesting!")
                return

            if selected_backtesting_stocks == "" or len(selected_backtesting_stocks) <= 0:
                messagebox.showerror("Selection Error", "Please select stocks to run in backtesting first!")
                return

            if selected_backtesting_analyzers_str == "" or len(selected_backtesting_analyzers_str) <= 0:
                continue_backtesting = messagebox.askyesno("Analyzer Selection",
                                                           "No additional analyzer ist selected! Do you want to start backtesting anyway?")
                if not continue_backtesting:
                    return

            data_backtesting_analyzers = []
            for ana in self.model.available_backtesting_analyzers_list.get():
                for selected_backtesting_analyzer_str in selected_backtesting_analyzers_str:
                    if selected_backtesting_analyzer_str in ana.__name__:
                        data_backtesting_analyzers.append(ana)

            available_backtesting_stocks_data = self.model.available_backtesting_stocks_list.get()
            selected_backtesting_stocks_data = []
            for selected_backtesting_stock_str in selected_backtesting_stocks:
                for available_backtesting_stock_data in available_backtesting_stocks_data:
                    if selected_backtesting_stock_str in available_backtesting_stock_data._name:
                        selected_backtesting_stocks_data.append(available_backtesting_stock_data)
                        pass

            req_params = StrategyFactory.get_required_parameters_with_default_parameters()
            at_objects = w.scrollable_frame_parameters.form.at_objects
            content_others = w.scrollable_frame_parameters.form.get_parameters(at_objects)

            if not self.accept_parameters_from_text(content_others, req_params):
                messagebox.showerror("Parameter file is not valid!",
                                     "Please choose a valid parameters file!")

            self.model.is_thread_running.set(True)
            logger.info("Backtesting started...")

            tbt = BacktraderWrapper()
            backtesting_parameters = self.model.analysis_parameters.get()["BacktestingParameters"]
            analysis_params = self.model.analysis_parameters.get()['Strategies'][strategy_selections[0]]
            # test only one strategy --> [0]
            cerebro, backtest_result = tbt.run_test(selected_backtesting_stocks_data,
                                                    data_backtesting_analyzers,
                                                    strategy_selections[0],
                                                    backtesting_parameters, analysis_params)

            insert_text_into_gui(self.view.Scrolledtext_analyzer_results, "", delete=True, start=1.0)

            # get items of analyzers and append it to the name
            analyzers = backtest_result[0].analyzers
            for analyzer in analyzers:
                ana_res = analyzer.get_analysis()
                items = list(ana_res.items())
                text_list = []
                for i in items:
                    text = ': '.join(str(e) for e in i)
                    text_list.append(text)

                final_text = '\n'.join(str(e) for e in text_list)
                insert_text_into_gui(self.view.Scrolledtext_analyzer_results,
                                     str(analyzer.__class__.__name__) + ":\n" + str(final_text) + "\n\n")

            portvalue = round(cerebro.broker.getvalue(), 2)
            pnl = round(portvalue - backtesting_parameters['initial_cash'], 2)

            # Print out the final result
            insert_text_into_gui(self.view.Scrolledtext_analyzer_results,
                                 'Final Portfolio Value: ${}'.format(portvalue) + "\n")
            insert_text_into_gui(self.view.Scrolledtext_analyzer_results,
                                 'Profit/Loss (rounded 2 places): ${}'.format(pnl))

            self.model.cerebro.set(cerebro)

        except Exception as e:
            logger.error("Exception while backtesting: " + str(e) + "\n" + str(traceback.format_exc()))

        self.model.is_thread_running.set(False)
        logger.info("Backtesting finished.")

    def accept_parameters_from_text(self, params_dict, required_parameters):
        """
        Method to accept the changes in the scrolled text for the parameters,
         if the shape and keys of parameters dict is same as required parameters dict.
        :return: True, if parameters are valid and updated.
        """
        try:
            if isinstance(params_dict, dict):
                for param_key in params_dict.keys():
                    if not param_key in required_parameters.keys() or len(params_dict[param_key]) <= 0:
                        logger.error("Parameter keys faulty, please insert correct parameters!")
                        return False

                    if not have_dicts_same_shape(required_parameters, params_dict):
                        logger.error("Parameter shapes are faulty, please insert correct parameters!")
                        return False

                self.model.analysis_parameters.clear()
                self.model.analysis_parameters.update(params_dict)
                self.model.available_strategies_list.clear()
                for item in params_dict['Strategies']:
                    self.model.available_strategies_list.append(item)
                logger.info("Analysis parameters Read")
            else:
                logger.error("Parameters are no dict, please insert correct parameters!")
                return False

        except Exception as e:
            logger.error("Exception while opening result stock: " + str(e) + "\n" + str(traceback.format_exc()))
            return False

        return True

    def load_analysis_parameters_from_file(self, file_path, required_parameters):
        """
        Loads the parameters into the GUI from a given filepath and file.
        :param required_parameters: a dict with all required parameters, must be all in file
        :param file_path: file path and name as string to load file
        :return: nothing
        """
        try:
            with open(file_path, "rb") as f:
                items = pickle.load(f)
                self.current_parameterfile = file_path
                if not self.accept_parameters_from_text(items, required_parameters):
                    override_params = messagebox.askyesno("Parameter file is not valid!",
                                                          "Do you want to CREATE a new file with default parameters?")

                    if override_params:
                        self.model.analysis_parameters.clear()
                        self.model.analysis_parameters.update(required_parameters)
                        self.model.available_strategies_list.clear()
                        for item in required_parameters['Strategies']:
                            self.model.available_strategies_list.append(item)

        except Exception as e:
            messagebox.showerror("Parameter file is not valid!",
                                 "Please choose a valid parameters file:" + str(e) + "\n" + str(traceback.format_exc()))
            logger.error(
                "Exception while loading other parameter from file: " + str(e) + "\n" + str(traceback.format_exc()))
            return

    def dump_analysis_parameters_to_file(self, file_path, params_dict, required_parameters=None):
        """
        Dumps the parameters to the given file, if the parameters shape is equal to required parameters.
        :param required_parameters: required parameters dict (shape is important for check)
        :param params_dict: the content to dump as string
        :param file_path: file path + name to dump to
        :return: -
        """

        if required_parameters is None or self.accept_parameters_from_text(params_dict, required_parameters):
            with open(file_path, "wb") as f:
                pickle.dump(params_dict, f)
                logger.info("Parameters Saved")
        else:
            messagebox.showerror("Parameter file is not valid!",
                                 "Please choose a valid parameters file!")

    # event handlers
    def quit_button_pressed(self):
        self.parent.destroy()

    def analysis_parameters_changed(self):
        parameters = self.model.analysis_parameters.get()
        try:
            w.TPanedwindow2_p2_parameters.destroy()
        except Exception as e:
            pass
        w.TPanedwindow2_p2_parameters = Labelframe(text='Parameters')
        w.TPanedwindow2.add(w.TPanedwindow2_p2_parameters)
        w.scrollable_frame_parameters = ScrollableFrame(w.TPanedwindow2_p2_parameters)
        w.scrollable_frame_parameters.populateFormParameters(parameters)

    def available_strategies_changed(self):
        insert_text_into_gui(w.Scrolledlistbox_selectStrategy, "", delete=True, start=0)
        # model internally chages and needs to signal a change
        available_strategies_list = self.model.available_strategies_list.get()
        for available_strategy in available_strategies_list:
            insert_text_into_gui(w.Scrolledlistbox_selectStrategy, available_strategy)

    def is_thread_running_changed(self):
        buttons = [w.ButtonRunStrategyRepetitive, w.ButtonRunStrategy, w.b_run_backtest, w.b_open_results_new_wd,
                   w.b_open_results_new_wd]
        if self.model.is_thread_running.get():
            set_buttons_state(buttons, 'disabled')
        else:
            set_buttons_state(buttons, 'normal')

    def result_stock_data_container_list_changed(self):
        """
        Update the columns and data of the view, of stock data container list changed.
        Additionally, it adds the not already available columns to the MvcModel and fill not available columns with dummy.
        :return: -
        """
        tree = w.Scrolledtreeview1
        tree.delete(*tree.get_children())
        stock_data_container_list = self.model.result_stock_data_container_list.get()

        for result_container in stock_data_container_list:
            try:
                is_updated = self.model.update_column_list(result_container.get_names_and_values().keys())

                if is_updated:
                    init_result_table(self.view.Scrolledtreeview1, self.model.get_column_list())

                GuiUtils.insert_into_treeview(self.view.Scrolledtreeview1, self.model.get_column_list(),
                                              result_container.get_names_and_values(), "Stock")

                # append all COLUMNS to file --> new layout leads to new line with header
                FileUtils.append_text_list_to_file(self.model.get_column_list(),
                                                   GlobalVariables.get_data_files_path() + "ScreeningResults.csv",
                                                   True, ",")

                # append VALUES to file
                values = result_container.get_names_and_values().values()
                text = ','.join(str(e) for e in values)
                FileUtils.append_textline_to_file(text,
                                                  GlobalVariables.get_data_files_path() + "ScreeningResults.csv",
                                                  True)

            except Exception as e:
                logger.error("Exception: " + str(e) + "\n" + str(traceback.format_exc()))
                continue

    def backtesting_stocks_list_changed(self):
        """
        Update the columns and data of the view, of stock data container list changed.
        Additionally, it adds the not already available columns to the MvcModel and fill not available columns with dummy.
        :return: -
        """
        insert_text_into_gui(w.sl_bt_select_stocks, "", delete=True, start=0)
        # model internally chages and needs to signal a change
        available_stocks = self.model.available_backtesting_stocks_list.get()
        for available_stock in available_stocks:
            insert_text_into_gui(w.sl_bt_select_stocks, available_stock._name)

    def backtesting_analyzers_list_changed(self):
        insert_text_into_gui(w.sb_select_analyzers, "", delete=True, start=0)
        # model internally chages and needs to signal a change
        backtesting_analyzers_list = self.model.available_backtesting_analyzers_list.get()
        for backtesting_analyzer in backtesting_analyzers_list:
            insert_text_into_gui(w.sb_select_analyzers, str(backtesting_analyzer.__name__))

    def cerebro_result_changed(self):
        # just the same as button pressed --> can not be called directly because backtesting is another thread
        # and plot can just be called in main tread
        # TODO is not working anyway
        # self.view.b_open_results_new_wd.invoke()
        pass

    def plot_backtesting(self):
        cerebro = self.model.cerebro.get()
        if cerebro is None:
            messagebox.showerror("Plot error", "There is no backtesting result to plot! Run a backtest first")
        else:
            cerebro.plot(style='candlestick', barup='green', bardown='red')

    def listbox_onselect_select_strategy(self, evt):
        # Note here that Tkinter passes an event object to listbox_onselect_select_strategy()
        selected_text_list = evaluate_list_box_selection(evt, "You selected items in strategy selection: ",
                                                         self.view.Scrolledlistbox_selectStrategy)
        self.model.selected_strategies_list.set(selected_text_list)

    def listbox_onselect_select_backtesting_stocks(self, evt):
        selected_text_list = evaluate_list_box_selection(evt, "You selected following stocks for backtesting: ",
                                                         self.view.sl_bt_select_stocks)
        self.model.selected_backtesting_stocks_list.set(selected_text_list)

    def listbox_onselect_select_backtesting_analyzers(self, evt):
        selected_text_list = evaluate_list_box_selection(evt, "You selected following analyzers for backtesting: ",
                                                         self.view.sb_select_analyzers)
        self.model.selected_backtesting_analyzers_list.set(selected_text_list)

    def load_backtesting_stocks_from_file(self, multi_file_path):
        data_list = []

        for file_path in multi_file_path:
            # now you can call it directly with basename
            stock_name = basename(file_path)
            data = btfeeds.GenericCSVData(
                name=stock_name,
                dataname=file_path,
                dtformat='%Y-%m-%d',
                # TODO fromdate=datetime.datetime(2000, 1, 1),
                # TODO todate=datetime.datetime(2000, 12, 31),
                nullvalue=0.0,
                datetime=0,
                open=1, high=2, low=3,
                close=4, volume=5,
                openinterest=-1)

            data_list.append(data)

        self.model.available_backtesting_stocks_list.set(data_list)
        logger.info("Backtesting stocks read")


def init(top, gui, *args, **kwargs):
    logging.basicConfig(level=logging.INFO)
    global w, top_level, root, app
    w = gui
    top_level = top
    root = top
    app = MyController(root, w)

    # ########################
    try:
        # load the last saved file path
        req_params = StrategyFactory.get_required_parameters_with_default_parameters()
        last_used_parameter_file_path = GlobalVariables.get_last_used_parameter_file()

        config = configparser.ConfigParser()
        config.read(last_used_parameter_file_path)

        # param_file = ast.literal_eval(config["Parameters"]['parameterfile'])
        param_file = (config["Parameters"]['parameterfile'])
        app.load_analysis_parameters_from_file(param_file, req_params)

        # TODO
        multi_file_path_str = config["Parameters"]['backteststockselection']
        if "," in multi_file_path_str:
            multi_file_path = multi_file_path_str.split(',')
        else:
            multi_file_path = multi_file_path_str
        # multi_file_path = ast.literal_eval(multi_file_path_str)
        app.load_backtesting_stocks_from_file(multi_file_path)

    except FileNotFoundError as fnfe:
        override_params = messagebox.askyesno("Last saved file is not found!",
                                              "Do you want to CREATE a new file?")

        # TODO
    except Exception as e:
        logger.error("Exception while opening last saved file path: " + str(e) + "\n" + str(traceback.format_exc()))

    # ########################
    return app


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


def save_analysis_parameters():
    file_path = filedialog.asksaveasfilename(initialdir=GlobalVariables.get_data_files_path(),
                                             filetypes=[("Pickle Dumps", "*.pickle")], defaultextension='.pickle',
                                             title="Select pickle parameterfile")

    at_objects = w.scrollable_frame_parameters.form.at_objects
    all_txt = w.scrollable_frame_parameters.form.get_parameters(at_objects)
    req_params = StrategyFactory.get_required_parameters_with_default_parameters()

    app.dump_analysis_parameters_to_file(file_path, all_txt, req_params)

    save_last_used_parameter_file()


def save_last_used_parameter_file():
    last_used_parameter_file_path = GlobalVariables.get_last_used_parameter_file()
    config = configparser.ConfigParser()
    curr_file = app.current_parameterfile

    data_files_path = GlobalVariables.get_data_files_path()
    backtest_stocks = app.model.available_backtesting_stocks_list.get()

    str_stocks = ','.join(str(data_files_path + stock._name) for stock in backtest_stocks)

    config["Parameters"] = {'parameterfile': curr_file,
                            'backteststockselection': str_stocks}

    with open(last_used_parameter_file_path, 'w') as configfile:
        config.write(configfile)


def quit():
    app.quit_button_pressed()


def edit():
    pass


def load_analysis_parameters():
    file_path = filedialog.askopenfilename(initialdir=GlobalVariables.get_data_files_path(),
                                           title="Select pickle parameterfile",
                                           filetypes=[("Pickle Dumps", "*.pickle")], defaultextension='.pickle')

    req_params = StrategyFactory.get_required_parameters_with_default_parameters()
    app.load_analysis_parameters_from_file(file_path, req_params)


def load_backtesting_stocks():
    multi_file_path = list(filedialog.askopenfilenames(initialdir=GlobalVariables.get_data_files_path(),
                                                       title="Select multiple stockdatafiles for backtesting",
                                                       filetypes=[("CSV-Files", "*.csv"), ("Text-Files", "*.txt")],
                                                       defaultextension='.csv'))

    app.load_backtesting_stocks_from_file(multi_file_path)


def init_result_table(tree_view, columns):
    if columns is not None and len(columns) > 0:

        col_2 = ["Item"]
        col_2.extend(columns)
        tree_view.configure(columns=col_2)

        for i in range(0, len(col_2)):
            heading_num = "#" + str(i)
            tree_view.heading(heading_num, text=col_2[i], anchor="center")

            if len(col_2[i]) > 8:  # TODO begründen / kommentieren
                tree_view.column(heading_num, width="200")
            else:
                tree_view.column(heading_num, width="100")
            tree_view.column(heading_num, minwidth="20")
            tree_view.column(heading_num, anchor="w")


def insert_text_into_gui(element, text, delete=False, start=1.0, end=END):
    """
    optionally deletes the given element and optionally insert text into given element.
    :param element: element to insert into (ex: Scrolledtext)
    :param text: text to insert
    :param delete: true, if delete content first
    :param start: start case, ex.: 1.0 or 0
    :param end: END tag
    :return: nothing
    """
    try:
        if delete:
            element.delete(start, end)
        if text is not None and len(text) > 0:
            element.insert(end, text)

        element.see("end")
    except Exception as e:
        logger.error("Can not insert text into gui: " + str(e) + "\n" + str(traceback.format_exc()))


class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame):
        self.frame = frame

        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText(frame, state='normal', height=5)
        self.scrolled_text.place(relx=0.01, rely=0.01, relheight=0.97, relwidth=0.98)
        self.scrolled_text.configure(wrap=NONE)
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)


class QueueHandler(logging.Handler):
    """Class to send logging records to a queue
    It can be used from different threads
    The ConsoleUi class polls this queue to display records in a ScrolledText widget
    """

    # Example from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06
    # (https://stackoverflow.com/questions/13318742/python-logging-to-tkinter-text-widget) is not thread safe!
    # See https://stackoverflow.com/questions/43909849/tkinter-python-crashes-on-new-thread-trying-to-log-on-main-thread

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)
