import traceback

from Utils.common_utils import print_err_message


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

        # TODO des vl gscheida lösen
        # enables all columns to sort by click on col header
        # for i in range(len(values_to_insert)):
        #    GuiUtils.treeview_sort_column(tree, i, True)
        GuiUtils.treeview_sort_column(tree, 1, True)

    @staticmethod
    def treeview_sort_column(tv, col, reverse):
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

            tv.heading(col, command=lambda: GuiUtils.treeview_sort_column(tv, col, not reverse))

        except Exception as e:
            print_err_message("Could not sort the given treeview!", e,
                              str(traceback.format_exc()))
