import tkinter as tk
from string import ascii_uppercase
from tkinter import *


# https://stackoverflow.com/questions/11047803/creating-a-table-look-a-like-tkinter/11049650#11049650
class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        t = SimpleTable(self, 10, -1, ["Stock name", "ticker", "Signal", "Reason"])
        t.pack(side="top", fill="x")
        t.set(1,0,"Hello, world")
        #t.set_row(3, ["t", "t", "B", "test"])
        #t.pack(side="top", fill="x")

class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=-1, header=[], cell_object=tk.Entry):
        # use black background so it "peeks through" to
        # form grid lines
        if cell_object != tk.Entry: # TODO and cell_object != tk.Label:
            raise NotImplementedError("Cell object only entry or label")

        # 0 or -1 --> auto set due to header length
        if columns <= 0:
            columns = len(header)

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
        row = row + 1
        widget = self._widgets[row][column] # TODO +1 because of header [0]
        #widget.configure(text=value)
        widget.delete(0, END)
        widget.insert(0, value)

    def set_row(self, row, column_content):
        for x in range(0, len(column_content)):
            self.set(row, x, column_content[x])




if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()
