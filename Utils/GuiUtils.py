import traceback

from Utils.Logger_Instance import logger


class GuiUtils:

    @staticmethod
    def insert_into_treeview(tree, column_list, names_and_values, tree_text="-"):
        values_to_insert = []
        for col in column_list:
            try:
                if col in names_and_values.keys():
                    values_to_insert.append(names_and_values[col])
                else:
                    values_to_insert.append("-")
            except Exception as e:
                values_to_insert.append("-")

        for col in names_and_values.keys():
            try:
                if col not in column_list:
                    values_to_insert.append(names_and_values[col])
            except Exception as e:
                pass

        tree.insert('', 'end', text=tree_text, values=values_to_insert)

        # enables all columns to sort by click on col header
        for i in range(len(values_to_insert)):
            GuiUtils.treeview_add_header_sort_column(tree, i, True)

    @staticmethod
    def _treeview_sort_column(tv, col, reverse):
        """
        https://stackoverflow.com/questions/1966929/tk-treeview-column-sort
        :param tv: tree view to sort
        :param col: column index to sort
        :param reverse:  True: reverse sort
        :return: -
        """
        try:
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            try:
                l.sort(key=lambda t: float(t[0]), reverse=reverse)
            except ValueError as e:
                l.sort(reverse=reverse)

            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)

            tv.heading(col, command=lambda: GuiUtils._treeview_sort_column(tv, col, not reverse))

        except Exception as e:
            logger.error("Exception Could not sort the given treeview: " + str(e) + "\n" + str(traceback.format_exc()))

    @staticmethod
    def treeview_add_header_sort_column(tv, col, reverse):
        """
        Adds a sort function to header
        https://stackoverflow.com/questions/1966929/tk-treeview-column-sort
        :param tv: tree view to sort
        :param col: column index to sort
        :param reverse:  True: reverse sort
        :return: -
        """
        try:
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            tv.heading(col, command=lambda: GuiUtils._treeview_sort_column(tv, col, not reverse))

        except Exception as e:
            logger.error("Exception Could not sort the given treeview: " + str(e) + "\n" + str(traceback.format_exc()))

    @staticmethod
    def evaluate_list_box_selection(evt, log_text, own_widget=None):
        widget = evt.widget

        if own_widget is None or own_widget is widget:
            try:
                selected_text_list = [widget.get(i) for i in widget.curselection()]
            except Exception as e:
                logger.error("Selection failed:" + str(e) + "\n" + str(traceback.format_exc()))
                selected_text_list = []

            logger.info(log_text + str(selected_text_list))
            return selected_text_list

    @staticmethod
    def set_buttons_state(buttons, state):
        """
        Set button state, or buttons state as list
        :param buttons: single items or list
        :param state: state as text
        :return: nothing
        """

        if isinstance(buttons, list):
            for button in buttons:
                button['state'] = state
        else:
            # only single button
            buttons['state'] = state
