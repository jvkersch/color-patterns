"""
Simple pattern editor example.

"""

import numpy as np

from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

from traits.api import Array, HasTraits, Int, on_trait_change
from traitsui.api import HGroup, VGroup, Item, View

from patterns.checker_board import CheckerBoardEditor


class MainWindow(HasTraits):

    array = Array

    rows = Int

    columns = Int

    view = View(
        HGroup(
            VGroup(
                Item('rows'),
                Item('columns'),
                label='Array Dimensions',
                show_border=True,
            ),
            Item('array', editor=CheckerBoardEditor()),
        ),
        resizable=True
    )

    def _array_default(self):
        return np.array([[False, True], [True, False], [True, True]])

    def _rows_default(self):
        return self.array.shape[0]

    def _columns_default(self):
        return self.array.shape[1]

    @on_trait_change('rows, columns')
    def _update_array_size(self):
        new_array = np.zeros((self.rows, self.columns), dtype=bool)
        old_rows, old_columns = self.array.shape
        rows = min(old_rows, self.rows)
        columns = min(old_columns, self.columns)
        new_array[:rows, :columns] = self.array[:rows, :columns]
        self.array = new_array


if __name__ == '__main__':
    main = MainWindow()
    main.configure_traits()
