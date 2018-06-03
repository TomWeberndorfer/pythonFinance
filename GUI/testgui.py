##Some points to mention...
##
##The model knows nothing about the view or the controller.
##The view knows nothing about the controller or the model.
##The controller understands both the model and the view.
##
##The model uses observables, essentially when important data is changed,
##any interested listener gets notified through a callback mechanism.
##
##The following opens up two windows, one that reports how much money you
##have, and one that has two buttons, one to add money and one to remove
##money.
##
##The important thing is that the controller is set up to monitor changes
##in the model.  In this case the controller notices that you clicked a
##button and modifies the money in the model which then sends out a
##message that it has changed.  The controller notices this and updates
##the widgets.
##
##The cool thing is that anything modifying the model will notify the
##controller.  In this case it is the controller modifying the model, but it
##could be anything else, even another controller off in the distance
##looking at something else.
##
##The main idea is that you give a controller the model and view that it
##needs, but the model's can be shared between controllers so that when
##the model is updated, all associated views are updated. -Brian Kelley
##
## following is a Tkinter approximation of the original example.

import tkinter as tk


class Observable:
    def __init__(self, initialValue=None):
        self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

    def _docallbacks(self):
        for func in self.callbacks:
            func(self.data)

    def set(self, data):
        self.data = data
        self._docallbacks()

    def get(self):
        return self.data

    def unset(self):
        self.data = None


class Model:
    def __init__(self):
        self.myMoney = Observable(0)
        self.available_stock_indices = Observable(["CDAX", "SP500", "Test1"])  # TODO # list with stock indices (DAX,..)

    def addMoney(self, value):
        self.myMoney.set(self.myMoney.get() + value)

    def removeMoney(self, value):
        self.myMoney.set(self.myMoney.get() - value)

    def set_available_stock_indices(self, available_stock_indices):
        t1 = self.available_stock_indices.get()
        t1.append(available_stock_indices)
        self.available_stock_indices.set(t1)


class View(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        tk.Label(self, text='My Money').pack(side='left')
        self.moneyCtrl = tk.Entry(self, width=80)
        self.moneyCtrl.pack(side='left')
        self.addButton = tk.Button(self, text='Add', width=8)
        self.addButton.pack(side='right')
        self.removeButton = tk.Button(self, text='Remove', width=8)
        self.removeButton.pack(side='right')

    def SetMoney(self, money):
        self.moneyCtrl.delete(0, 'end')
        self.moneyCtrl.insert('end', str(money))


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.model.myMoney.addCallback(self.MoneyChanged)
        self.model.available_stock_indices.addCallback(self.available_indices_changed)
        self.view1 = View(root)
        self.view1.addButton.config(command=self.add_available_indices)
        self.view1.removeButton.config(command=self.RemoveMoney)
        self.MoneyChanged(self.model.myMoney.get())
        self.available_indices_changed(self.model.available_stock_indices.get())

    def RemoveMoney(self):
        self.model.removeMoney(10)

    def add_available_indices(self):
        self.model.set_available_stock_indices("Test1")

    def available_indices_changed(self, money):
        self.view1.SetMoney(money)

    def MoneyChanged(self, money):
        self.view1.SetMoney(money)


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()