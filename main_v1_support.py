#! /usr/bin/env python
#
# Support module generated by PAGE version 4.9
# In conjunction with Tcl version 8.6
#    Jun 03, 2018 10:50:55 AM
import sys
import _pickle as pickle
import os
from tkinter import messagebox

from GUI.SimpleTable import SimpleTable
from GUI.main_v1 import global_filepath
from Main import run_screening
from Utils.news_utils import NewsUtils

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk

    py3 = 0
except ImportError:
    import tkinter.ttk as ttk

    py3 = 1

# TODO ev in config file -->  gui load
# immer ins main kopieren
# global ROOT_DIR
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# global global_filepath
# global_filepath = ROOT_DIR + '\\DataFiles\\'
# #TODO vom dataprovider lesen und dann zuweisen (irgendeine aktie abfragen)
# global glob_stock_data_labels_dict
# glob_stock_data_labels_dict = {'High': 'high', 'Low':'low', 'Open':'open',
#                                'Close':'close', 'Volume':'volume'}

class MyController:
    """
    Classs for the controlling of mvc design with gui
    """
    def __init__(self, parent):
        self.parent = parent
        self.model = MyModel(self)  # initializes the model
        self.view = w  # initializes the view
        # self.view.Match.config(command=self.all_parameter_dicts_changed)
        self.view.ButtonRunStrategy.config(command=self.start_screening)
        self.view.Scrolledlistbox_selectStrategy.bind('<<ListboxSelect>>', self.listbox_onselect)
        self.all_parameter_dicts_changed()
        self.available_strategies_changed()
        self.load_parameter_from_file()

    def start_screening(self):
        """
        Method to start the screening once
        :return: nothing, results are saved in the model.
        """
        selection_value = self.model.get_strategy_selection_value()

        if selection_value == "" or len(selection_value) <= 0:
            messagebox.showerror("Selection Error", "Please select a strategy first!")
        else:
            selected_strategy_params = self.model.get_all_parameter_dicts()[selection_value]
            stock_data_container_file_name = "stock_data_container_file.pickle"
            stock_data_container_file = global_filepath + stock_data_container_file_name
            last_date_time_file = global_filepath + "last_date_time.csv"
            data_source = 'iex'
            weeks_delta = 52  # one year in the past
            other_params = {'stock_data_container_file': stock_data_container_file, 'weeks_delta': weeks_delta,
                            'data_source': data_source, 'last_date_time_file': last_date_time_file}
            results = run_screening(selection_value, selected_strategy_params, other_params)
            self.model.extend_result_stock_data_container_list(results)


    def load_parameter_from_file(self):
        """
        Loads the parameters into the GUI from a given filepath and file.
        :return: nothing
        """
        self.model.clear_all_parameter_dicts()
        self.model.clear_list()

        try:
            with open(global_filepath + "ParameterFile.pickle", "rb") as f:
                items = pickle.load(f)
                self.model.add_to_all_parameter_dicts(items)
                for item in items:
                    self.model.add_to_available_strategies(item)

        except Exception as e:
            print(str(e))
            return

        self.model.add_to_log("Params Read")
        
    def insert_log(self, log_text):
        self.model.add_to_log(log_text)

    def dump_parameter_to_file(self):
        """
        dumps the parameters to a global given file
        :return:
        """
        content = self.view.Scrolledtext_params.get(1.0, END)
        import ast
        content_dict = ast.literal_eval(content)

        if content_dict == {}:
            messagebox.showerror("Parameters empty", "Please insert parameters")
        else:
            self.model.add_to_all_parameter_dicts(content_dict)
            with open(global_filepath + "ParameterFile.pickle", "wb") as f:
                pickle.dump(self.model.all_parameter_dicts, f)

            self.model.add_to_log("Params Saved")

    # event handlers
    def quitButtonPressed(self):
        self.parent.destroy()

    def add_button_pressed(self):
        self.model.add_to_available_strategies(self.view.entry_text.get())
        self.model.add_to_all_parameter_dicts({self.view.entry_text.get(): self.view.entry_text.get()})

    def clear_button_pressed(self):
        self.model.clear_list()

    def all_parameter_dicts_changed(self):
        w.Scrolledtext_params.delete(1.0, END)
        # model internally chages and needs to signal a change
        #TODO 11:
        parameters = self.model.get_all_parameter_dicts()
        self.insert_text_into_gui(w.Scrolledtext_params, str(parameters))
        #for key, value in parameters.items():
        #    w.Scrolledtext_params.insert(END, "{'" + key + "':" + str(value) + "}")
        #    w.Scrolledtext_params.insert(END, "\n")

    def log_changed_delegate(self):
        self.insert_text_into_gui(w.Scrolledtext_log, "", delete=True)
        logs = self.model.get_log()
        for log in logs:
            self.insert_text_into_gui(w.Scrolledtext_log, log)
            self.insert_text_into_gui(w.Scrolledtext_log, "\n")

    def available_strategies_changed(self):
        self.insert_text_into_gui(w.Scrolledlistbox_selectStrategy, "", delete=True, start=0)
        # model internally chages and needs to signal a change
        available_strategies_list = self.model.getList()
        for available_strategy in available_strategies_list:
            self.insert_text_into_gui(w.Scrolledlistbox_selectStrategy, available_strategy)

    def result_stock_data_container_list_changed(self):
        #self.insert_text_into_gui(w.Scrolledtext_Results, "", delete=True)
        # model internally chages and needs to signal a change
        stock_data_container_list = self.model.get_result_stock_data_container_list()
        #TODO des weg und treeview her
        print_str = NewsUtils.format_news_analysis_results(stock_data_container_list)
        print(print_str)
        #self.insert_text_into_gui(w.Scrolledtext_Results, print_str)

        tree = w.Scrolledtreeview1
        for res in stock_data_container_list:
            if res.stock_name is not None:
                pos_class = round(res.prob_dist.prob("pos"), 2)
                neg_class = round(res.prob_dist.prob("neg"), 2)
                if pos_class > neg_class:
                    recommendation_text = "BUY"
                else:
                    recommendation_text = "SELL"

            tree.insert('', 'end', text=recommendation_text, values=(res.stock_ticker, res.stock_name,
                                                                     res.stock_exchange, str(pos_class), str(neg_class),
                                                                     str(res.stock_current_prize),
                                                                     str(res.stock_target_price), res.orignal_news))

        treeview_sort_column(tree, 'Pos', False)

    def listbox_onselect(self, evt):
        # Note here that Tkinter passes an event object to listbox_onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print('You selected item %d: "%s"' % (index, value))
        self.model.set_strategy_selection_value(value)

    def insert_text_into_gui(self, element, text, delete=False, start=1.0, end=END):
        """
        optionally deletes the given element and optionally insert text into given element.
        :param element: element to insert into (ex: Scrolledtext)
        :param text: text to insert
        :param delete: true, if delete content first
        :param start: start case, ex.: 1.0 or 0
        :param end: END tag
        :return: nothing
        """
        if delete:
            element.delete(start, end)
        if text is not None and len(text) > 0:
            element.insert(end, text)



class MyModel:
    def __init__(self, vc):
        self.vc = vc
        self.available_strategies = [] #TODO ["SimplePatternNewsStrategy", "W52HighTechnicalStrategy"]
        #TODO verwenden
        self.program_parameter_dict = {'data_source': 'iex', 'weeks_delta': 52}
        self.all_parameter_dicts = {}
        w52hi_parameter_dict = {'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98}
        parameter_dict = {'news_threshold': 0.7, 'german_tagger': global_filepath + 'nltk_german_classifier_data.pickle'}
        #self.all_parameter_dicts = {'W52HighTechnicalStrategy': w52hi_parameter_dict, "SimplePatternNewsStrategy": parameter_dict}
        self.log_text = []
        self.strategy_selection_value = ""
        self.result_stock_data_container_list = []

    def get_result_stock_data_container_list(self):
        return self.result_stock_data_container_list

    def clear_result_stock_data_container_list(self):
        self.result_stock_data_container_list = []
        self.vc.result_stock_data_container_list_changed()

    def extend_result_stock_data_container_list(self, stock_data_container_list):
        self.result_stock_data_container_list.extend(stock_data_container_list)
        self.vc.result_stock_data_container_list_changed()

    def set_strategy_selection_value(self, value):
        self.strategy_selection_value = value

    def get_strategy_selection_value(self):
        return self.strategy_selection_value

    # Delegates-- Model would call this on internal change
    def all_parameter_dicts_changed(self):
        self.vc.all_parameter_dicts_changed()

    # setters and getters
    def get_all_parameter_dicts(self):
        return self.all_parameter_dicts

    def add_to_all_parameter_dicts(self, items):
        for key, value in items.items():
            self.all_parameter_dicts.update({key: value})
        self.all_parameter_dicts_changed()

    def clear_all_parameter_dicts(self):
        self.all_parameter_dicts = {}
        self.all_parameter_dicts_changed()

    # Delegates-- Model would call this on internal change
    def list_changed(self):
        self.vc.available_strategies_changed()

    # setters and getters
    def getList(self):
        return self.available_strategies

    def add_to_available_strategies(self, item):
        myList = self.available_strategies
        myList.append(item)
        self.available_strategies = myList
        self.list_changed()

    def clear_list(self):
        self.available_strategies = []
        self.list_changed()

    def add_to_log(self, log_text):
        self.log_text.append(log_text)
        self.log_changed()

    def log_changed(self):
        self.vc.log_changed_delegate()

    def get_log(self):
        return self.log_text



def init(top, gui, *args, **kwargs):
    global w, top_level, root, app
    w = gui
    top_level = top
    root = top

    app = MyController(root)

    #TODO wo anders
    tree = w.Scrolledtreeview1
    headings = ["Recommendation", "Stockname", "Ticker", "Stock Exchange", "Pos", "neg", "current value", "target price", "orig News"]
    tree['columns'] = headings
    for heading in range(len(headings)):
        tree.heading('#' + str(heading), text=headings[heading])


# todo ins gui utils
def treeview_sort_column(tv, col, reverse):
    """
    https://stackoverflow.com/questions/1966929/tk-treeview-column-sort
    :param tv:
    :param col:
    :param reverse:
    :return:
    """
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    try:
        l.sort(key=lambda t: int(t[0]), reverse=reverse)
        #      ^^^^^^^^^^^^^^^^^^^^^^^
    except ValueError:
        l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


def save():
    app.dump_parameter_from_file()


def quit():
    pass


def edit():
    pass


def load_params():
    app.load_parameter_from_file()


if __name__ == '__main__':
    import main_v1

    main_v1.vp_start_gui()
