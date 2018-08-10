import tkinter as tk
from tkinter import ttk, W, E

import tkinter as tk
from tkinter import ttk, W, E

from Utils.common_utils import is_float, is_int


class ParametersForm:

    def __init__(self, frame, params):
        self.frame = frame
        self.var_list = []
        self.my_col = 0
        self.my_row = 0
        self.at = {}
        self.at_objects = {}
        self.first_params = params

        my_col_2, my_row2, at, ao = self.rec(params, self.my_col, self.my_row)
        self.at = at
        self.at_objects = ao

        assert at == params

    def find_in_grid(self, row, column):
        for children in self.frame.children.values():
            info = children.grid_info()
            # note that rows and column numbers are stored as string
            if info['row'] == str(row) and info['column'] == str(column):
                return children
        return None

    def rec(self, params, my_col, my_row):
        my_col_2 = my_col
        all_txt = {}
        all_objects = {}

        if isinstance(params, dict):
            for key in params.keys():
                my_col_2 = my_col
                my_row = my_row + 1
                txt_var = key
                # ttk.Label(self.frame, textvariable=txt_var).grid(column=my_col, row=my_row, sticky=W)
                # ttk.Label(self.frame, text=txt_var).grid(column=my_col, row=my_row, sticky=W)
                tklab = ttk.Label(self.frame, text=txt_var)
                tklab.grid(column=my_col, row=my_row, sticky=W)
                # ttk.Label(self.frame, textvariable=self.testvar2).grid(column=my_col, row=my_row, sticky=W)
                my_col_2 = my_col_2 + 1

                my_col_2, my_row, txt, obj = self.rec(params[key], my_col_2, my_row)
                all_txt.update({txt_var: txt})
                all_objects.update({tklab: obj})
        else:
            # TODO
            # if isinstance(params, list):
            #     for entry in params:
            #         ttk.Label(self.frame, text=str(entry) + ": ").grid(column=my_col, row=my_row, sticky=W)
            #         my_col, my_row = self.rec(entry, my_col, my_row)
            #         my_row = my_row + 1
            # else:
            # ttk.Label(self.frame, text=str(params) + ": ").grid(column=my_col, row=my_row, sticky=W)
            # ttk.Entry(self.frame, textvariable="test23", width=25).grid(column=my_col, row=my_row,
            #                                                            sticky=(W, E))

            # tktxt = tk.Entry(self.frame, textvariable=self.testvar)
            tktxt = tk.Entry(self.frame)
            tktxt.grid(column=my_col, row=my_row, sticky=(W, E))
            tktxt.insert(tk.END, str(params))

            all_txt = params
            all_objects = tktxt
            my_row = my_row + 1

        return my_col_2, my_row, all_txt, all_objects

    def rec_objects(self, params, my_col, my_row):
        my_col_2 = my_col
        all_txt = {}

        if isinstance(params, dict):
            for key in params.keys():
                my_col_2 = my_col
                my_row = my_row + 1
                txt_var = key["text"]
                my_col_2 = my_col_2 + 1

                my_col_2, my_row, txt = self.rec_objects(params[key], my_col_2, my_row)
                all_txt.update({txt_var: txt})
        else:
            txt_entry = params.get()

            if is_int(txt_entry):
                all_txt = int(txt_entry)
            elif is_float(txt_entry):
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

    def get_parameters(self, at_objects, x=0, y=0):
        my_col_2, my_row, all_txt = self.rec_objects(at_objects, x, y)
        return all_txt
