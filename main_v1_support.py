#! /usr/bin/env python
#
# Support module generated by PAGE version 4.9
# In conjunction with Tcl version 8.6
#    Jun 03, 2018 10:50:55 AM
import _pickle as pickle
import queue
import tkinter as tk
import traceback
from threading import Thread
from tkinter import messagebox
import logging
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Labelframe

from GUI.ScrollableFrame import ScrollableFrame
from Strategies.StrategyFactory import StrategyFactory
from Utils.Logger_Instance import logger
from MvcModel import MvcModel
from StockAnalysis import run_analysis
from tkinter import *
import webbrowser as wb
import ast
from tkinter import filedialog

from Utils.GlobalVariables import *
from Utils.GuiUtils import GuiUtils
from Utils.common_utils import have_dicts_same_shape
from Utils.file_utils import FileUtils


class MyController:
    """
    Classs for the controlling of mvc design with gui
    """

    def __init__(self, parent, view):
        self.parent = parent
        self.model = MvcModel(self)  # initializes the model
        self.view = view  # initializes the view
        self.view.ButtonRunStrategy.config(command=self.start_screening)
        self.view.Scrolledlistbox_selectStrategy.bind('<<ListboxSelect>>', self.listbox_onselect)
        self.view.Scrolledtreeview1.bind("<Double-1>", self.on_double_click)
        self.available_strategies_changed()

        req_params = StrategyFactory.get_required_parameters_with_default_parameters()
        self.load_other_parameter_from_file(GlobalVariables.get_data_files_path() + "OtherParameterFile.pickle",
                                            req_params)
        self.other_params_changed()
        init_result_table(self.view.Scrolledtreeview1, self.model.get_column_list())
        self.console = ConsoleUi(self.view.Labelframe2)

    def on_double_click(self, event):
        """
        TODO beschreiben und fixe url weg
        :param event:
        :return:
        """
        try:
            cur_selection = self.view.Scrolledtreeview1.selection()[0]
            cur_stock = self.view.Scrolledtreeview1.item(cur_selection)

            # TODO je nachj container unterschiedlich 2 --> name is first
            stock_name = cur_stock['values'][2]
            url_to_open = "http://www.finanzen.at/suchergebnisse?_type=Aktien&_search="
            wb.open_new_tab(url_to_open + stock_name)
        except IndexError as e:
            pass  # nothing to do for index error (may clicked at header)
        except Exception as e:
            logger.error("Exception while opening result stock: " + str(e) + "\n" + str(traceback.format_exc()))

    def start_screening(self):
        """
        start the screening thread for NON blocking GUI.
        :return: nothing
        """
        if not self.model.get_is_thread_running():
            thread = Thread(target=self.screening)
            thread.start()

    def screening(self):
        """
        Method to start the screening once
        :return: nothing, results are saved in the model.
        """
        try:
            selection_values = self.model.get_strategy_selection_value()

            if selection_values == "" or len(selection_values) <= 0:
                messagebox.showerror("Selection Error", "Please select a strategy first!")
                return

            if not self.accept_parameters_from_text():
                return

            self.model.set_is_thread_running(True)
            logger.info("Screening started...")
            self.model.clear_result_stock_data_container_list()
            other_params = self.model.get_other_params()
            results = run_analysis(selection_values, other_params['Strategies'], other_params['OtherParameters'])

            self.model.extend_result_stock_data_container_list(results)
        except Exception as e:
            logger.error("Exception while screening: " + str(e) + "\n" + str(traceback.format_exc()))

        self.model.set_is_thread_running(False)

    def accept_parameters_from_text(self):
        """
        Method to accept the changes in the scrolled text for the parameters.
        :return: True, if parameters are valid and updated.
        """
        try:
            at_objects = w.scrollable_frame_parameters.form.at_objects
            content_others = w.scrollable_frame_parameters.form.get_parameters(at_objects)

            if content_others == {}:
                messagebox.showerror("Parameters empty", "Please insert parameters")
                return False

            self.model.clear_other_params()
            self.model.add_to_other_params(content_others)

        except Exception as e:
            messagebox.showerror("Parameters not valid", "Please insert valid parameters: " + str(e))
            return False

        return True

    def load_other_parameter_from_file(self, file_path, required_parameters):
        """
        Loads the parameters into the GUI from a given filepath and file.
        :param required_parameters: a dict with all required parameters, must be all in file
        :param file_path: file path and name as string to load file
        :return: nothing
        """
        try:
            with open(file_path, "rb") as f:
                items = pickle.load(f)
                if isinstance(items, dict) \
                        and 'OtherParameters' in items.keys() and len(items['OtherParameters']) > 0 \
                        and 'Strategies' in items.keys() and len(items['Strategies']) > 0 and \
                        have_dicts_same_shape(required_parameters, items['Strategies']):

                    self.model.clear_other_params()
                    self.model.add_to_other_params(items)
                    self.model.clear_available_strategies_list()
                    for item in items['Strategies']:
                        self.model.add_to_available_strategies(item)
                    logger.info("Parameters Read")

                else:
                    messagebox.showerror("Parameter file is not valid!",
                                         "Please choose a valid parameters file, with this data format:\n"
                                         + str(required_parameters) + "\n\n" + "Selected format is: \n"
                                         + str(items['Strategies']))

        except Exception as e:
            logger.error(
                "Exception while loading other parameter from file: " + str(e) + "\n" + str(traceback.format_exc()))
            return

    def dump_other_parameter_to_file(self,
                                     file_path=GlobalVariables.get_data_files_path() + "OtherParameterFile.pickle",
                                     content_others=""):
        """
        dumps the parameters to a global given file
        :param content_others: the content to dump as string
        :param file_path: file path + name to dump to
        :return: -
        """
        try:
            if isinstance(content_others, str):
                content_others_dict = ast.literal_eval(content_others)
            else:
                content_others_dict = content_others

            if content_others_dict == {}:
                messagebox.showerror("Parameters empty", "Please insert parameters")
            else:
                self.model.clear_other_params()
                self.model.add_to_other_params(content_others_dict)
                with open(file_path, "wb") as f:
                    params_dict = self.model.get_other_params()

                    if isinstance(params_dict, dict) \
                            and 'OtherParameters' in params_dict.keys() \
                            and len(params_dict['OtherParameters']) > 0 and 'Strategies' in params_dict.keys() \
                            and len(params_dict['Strategies']) > 0:

                        pickle.dump(params_dict, f)
                        logger.info("Parameters Saved")
                    else:
                        messagebox.showerror("Parameter file is not valid!",
                                             "Please choose a valid parameters file!")

        except Exception as e:
            logger.error("Exception while dump_other_parameter_to_file: " + str(e) + "\n" + str(traceback.format_exc()))
            return

    # event handlers
    def quit_button_pressed(self):
        self.parent.destroy()

    def other_params_changed(self):
        parameters = self.model.get_other_params()
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
        available_strategies_list = self.model.get_available_strategies()
        for available_strategy in available_strategies_list:
            insert_text_into_gui(w.Scrolledlistbox_selectStrategy, available_strategy)

    def is_thread_running_changed(self):
        if self.model.get_is_thread_running():
            w.ButtonRunStrategyRepetitive['state'] = 'disabled'
            w.ButtonRunStrategy['state'] = 'disabled'
        else:
            w.ButtonRunStrategy['state'] = 'normal'
            w.ButtonRunStrategyRepetitive['state'] = 'normal'

    def result_stock_data_container_list_changed(self):
        """
        Update the columns and data of the view, of stock data container list changed.
        Additionally, it adds the not already available columns to the MvcModel and fill not available columns with dummy.
        :return: -
        """

        tree = w.Scrolledtreeview1
        tree.delete(*tree.get_children())
        stock_data_container_list = self.model.get_result_stock_data_container_list()

        for result_container in stock_data_container_list:
            try:
                is_updated = self.model.update_column_list(result_container.get_names_and_values().keys())

                if is_updated:
                    init_result_table(self.view.Scrolledtreeview1, self.model.get_column_list())

                GuiUtils.insert_into_treeview(self.view.Scrolledtreeview1, self.model.get_column_list(),
                                              result_container.get_names_and_values(), "Stock")

                # append all columns to file --> new layout leads to new line with header
                FileUtils.append_text_list_to_file(self.model.get_column_list(),
                                                   GlobalVariables.get_data_files_path() + "ScreeningResults.csv",
                                                   True, ",")

                values = result_container.get_names_and_values().values()
                text = ','.join(str(e) for e in values)

                FileUtils.append_textline_to_file(text,
                                                  GlobalVariables.get_data_files_path() + "ScreeningResults.csv",
                                                  True)

            except Exception as e:
                logger.error("Exception: " + str(e) + "\n" + str(traceback.format_exc()))
                continue

    def listbox_onselect(self, evt):
        # Note here that Tkinter passes an event object to listbox_onselect()
        widget = evt.widget
        try:
            selected_text_list = [widget.get(i) for i in widget.curselection()]
        except Exception as e:
            selected_text_list = []

        logger.info("You selected items: " + str(selected_text_list))
        self.model.set_strategy_selection_value(selected_text_list)


def init(top, gui, *args, **kwargs):
    # TODO loglevel logging level
    logging.basicConfig(level=logging.INFO)
    global w, top_level, root, app
    w = gui
    top_level = top
    root = top
    app = MyController(root, w)

    return app


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


def save_other_params():
    file_path = filedialog.asksaveasfilename(initialdir=GlobalVariables.get_data_files_path(),
                                             filetypes=[("Pickle Dumps", "*.pickle")], defaultextension='.pickle',
                                             title="Select pickle other parameterfile")

    at_objects = w.scrollable_frame_parameters.form.at_objects
    all_txt = w.scrollable_frame_parameters.form.get_parameters(at_objects)

    app.dump_other_parameter_to_file(file_path, all_txt)


def quit():
    app.quit_button_pressed()


def edit():
    pass


def load_other_params():
    file_path = filedialog.askopenfilename(initialdir=GlobalVariables.get_data_files_path(),
                                           title="Select pickle other parameterfile",
                                           filetypes=[("Pickle Dumps", "*.pickle")], defaultextension='.pickle')

    req_params = StrategyFactory.get_required_parameters_with_default_parameters()
    app.load_other_parameter_from_file(file_path, req_params)


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
            tree_view.column(heading_num, stretch="1")
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
