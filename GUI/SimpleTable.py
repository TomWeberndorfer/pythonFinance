import tkinter as tk
from string import ascii_uppercase
from tkinter import *


# https://stackoverflow.com/questions/11047803/creating-a-table-look-a-like-tkinter/11049650#11049650
class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        t = SimpleTable(self, 10, 2, ["Stock name", "ticker"])
        t.pack(side="top", fill="x")
        # t.set(0,0,"Hello, world")


class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=2, header=[], cell_object=tk.Entry):
        # use black background so it "peeks through" to
        # form grid lines
        if cell_object != tk.Entry and cell_object != tk.Label:
            raise NotImplementedError("Cell object only entry or label")

        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []

            for column in range(columns):
                # for the headers in row 0
                if row == 0:
                    if not header:
                        label_text = ascii_uppercase[column]
                    else:
                        label_text = header[column]
                else:
                    label_text = "%s/%s" % (row, column)

                obj = cell_object(self, text=label_text, relief=RIDGE)

                if cell_object != tk.Label:
                    obj.insert(END, label_text)

                relief = RIDGE
                obj.grid(row=row, column=column, sticky=NSEW)
                current_row.append(obj)
                self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)


if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()
