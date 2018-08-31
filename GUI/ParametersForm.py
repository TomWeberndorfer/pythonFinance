import tkinter as tk
from tkinter import ttk, W, E

import tkinter as tk
from tkinter import ttk, W, E

from Utils.CommonUtils import CommonUtils


class ParametersForm:

    def __init__(self, frame, params_dict):
        """
        Initialises the parameter form with labels for every dict key and entry for every dict value of the params dict.
        :param frame: Frame to insert form.
        :param params_dict: Dictionary with parameters to create a form.
        """
        self.frame = frame
        self.var_list = []
        self.my_col = 0
        self.my_row = 0
        self.at = {}
        self.at_objects = {}
        self.first_params = params_dict

        my_col_2, my_row2, at, ao = self._create_parameter_labels_and_entries_recursive(params_dict, self.my_col,
                                                                                        self.my_row)
        self.at = at
        self.at_objects = ao

        # parameters dict goes in must the same as created from form gui
        assert at == params_dict

    def find_in_grid(self, row, column):
        for children in self.frame.children.values():
            info = children.grid_info()
            # note that rows and column numbers are stored as string
            if info['row'] == str(row) and info['column'] == str(column):
                return children
        return None

    def _create_parameter_labels_and_entries_recursive(self, params, my_col, my_row):
        """
        Method creates a form with labels and entries recursive.
        :param params:
        :param my_col: column to start in a grid
        :param my_row: row to start in a grid
        :return: the current column, current row, all text recreated from params as dict and all objects created as dict
        """
        my_col_2 = my_col
        all_txt = {}
        all_objects = {}

        if isinstance(params, dict):
            for key in params.keys():
                my_col_2 = my_col
                my_row = my_row + 1
                txt_var = key
                tklab = ttk.Label(self.frame, text=txt_var)
                tklab.grid(column=my_col, row=my_row, sticky=W)
                my_col_2 = my_col_2 + 1

                my_col_2, my_row, txt, obj = self._create_parameter_labels_and_entries_recursive(params[key], my_col_2,
                                                                                                 my_row)
                all_txt.update({txt_var: txt})
                all_objects.update({tklab: obj})
        else:
            tktxt = tk.Entry(self.frame, width=40)
            tktxt.grid(column=my_col, row=my_row, sticky=(W, E))
            tktxt.insert(tk.END, str(params))

            all_txt = params
            all_objects = tktxt
            my_row = my_row + 1

        return my_col_2, my_row, all_txt, all_objects

    def _read_objects_as_dict_recursive(self, params, my_col, my_row):
        """
        Reads the objects from params and returns the parameters as dictionary.
        :param params:
        :param my_col:
        :param my_row:
        :return:
        """
        my_col_2 = my_col
        all_txt = {}

        if isinstance(params, dict):
            for key in params.keys():
                my_col_2 = my_col
                my_row = my_row + 1
                txt_var = key["text"]
                my_col_2 = my_col_2 + 1

                my_col_2, my_row, txt = self._read_objects_as_dict_recursive(params[key], my_col_2, my_row)
                all_txt.update({txt_var: txt})
        else:
            txt_entry = params.get()

            if CommonUtils.is_int(txt_entry):
                all_txt = int(txt_entry)
            elif CommonUtils.is_float(txt_entry):
                all_txt = float(txt_entry)
            elif isinstance(txt_entry, str):
                if txt_entry in 'True':
                    all_txt = True
                else:
                    if txt_entry in 'False':
                        all_txt = False
                    else:
                        all_txt = txt_entry

            my_row = my_row + 1

        return my_col_2, my_row, all_txt

    def get_parameters(self, at_objects, col=0, row=0):
        """
        Get the parameters from the parameters form as parameter dictionary.
        :param at_objects:
        :param col: column to start
        :param row: row to start
        :return: parameter dict of the parameter form (labels and entries)
        """
        my_col_2, my_row, all_txt = self._read_objects_as_dict_recursive(at_objects, col, row)
        return all_txt
