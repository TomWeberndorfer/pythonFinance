'''
Created on Mar 21, 2016

@author: Bill Begueradj
'''
import tkinter
from tkinter import *
from tkinter import ttk

class Begueradj(Frame):
    '''
    classdocs
    '''
    def __init__(self, parent):
        '''
        Constructor
        '''
        Frame.__init__(self, parent)
        self.parent=parent
        self.initialize_user_interface()

    def initialize_user_interface(self):
        """Draw a user interface allowing the user to type
        items and insert them into the treeview
        """
        self.parent.title("Canvas Test")
        self.parent.grid_rowconfigure(0,weight=1)
        self.parent.grid_columnconfigure(0,weight=1)
        self.parent.config(background="lavender")


        # Define the different GUI widgets
        self.dose_label = Label(self.parent, text = "Dose:")
        self.dose_entry = Entry(self.parent)
        self.dose_label.grid(row = 0, column = 0, sticky = W)
        self.dose_entry.grid(row = 0, column = 1)

        self.modified_label = Label(self.parent, text = "Date Modified:")
        self.modified_entry = Entry(self.parent)
        self.modified_label.grid(row = 1, column = 0, sticky = W)
        self.modified_entry.grid(row = 1, column = 1)

        self.submit_button = Button(self.parent, text = "Insert", command = self.insert_data)
        self.submit_button.grid(row = 2, column = 1, sticky = W)
        self.exit_button = Button(self.parent, text = "Exit", command = self.parent.quit)
        self.exit_button.grid(row = 0, column = 3)

        # Set the treeview
        self.tree = ttk.Treeview( self.parent, columns=('Dose', 'Modification date'))
        self.tree.heading('#0', text='Item')
        self.tree.heading('#1', text='Dose')
        self.tree.heading('#2', text='Modification Date')
        self.tree.column('#1', stretch=YES)
        self.tree.column('#2', stretch=YES)
        self.tree.column('#0', stretch=YES)
        self.tree.grid(row=4, columnspan=4, sticky='nsew')
        self.treeview = self.tree
        # Initialize the counter
        self.i = 0

        self.treeview.insert('', 'end', text="Item_a",
                             values=("a" + " mg", "a"))

        self.treeview.insert('', 'end', text="Item_c",
                             values=("c" + " mg", "c"))

        self.treeview.insert('', 'end', text="Item_b",
                             values=("b" + " mg", "b"))


        treeview_sort_column(self.treeview, 'Dose', False)


    def insert_data(self):
        """
        Insertion method.
        """
        self.treeview.insert('', 'end', text="Item_"+str(self.i), values=(self.dose_entry.get()+" mg", self.modified_entry.get()))
        # Increment counter
        self.i = self.i + 1

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    try:
        l.sort(key=lambda t: int(t[0]), reverse=reverse)
        #      ^^^^^^^^^^^^^^^^^^^^^^^
    except ValueError:
        l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

def main():
    root=Tk()
    d=Begueradj(root)
    root.mainloop()

if __name__=="__main__":
    main()