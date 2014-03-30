"""
Simple facades around checkerboard models, adapted for various purposes.


"""

import numpy as np

from traits.api import Array, HasTraits, Int, on_trait_change


class Binding(HasTraits):

    rows = Int

    columns = Int

    array = Array

    def _array_default(self):
        return np.array([[False, True], [True, False], [True, True]])

    def _rows_default(self):
        return self.array.shape[0]

    def _columns_default(self):
        return self.array.shape[1]

    @on_trait_change('rows, columns')
    def _update_array_size(self):
        # TODO Refactor this?
        new_array = np.zeros((self.rows, self.columns), dtype=bool)
        old_rows, old_columns = self.array.shape
        rows = min(old_rows, self.rows)
        columns = min(old_columns, self.columns)
        new_array[:rows, :columns] = self.array[:rows, :columns]
        self.array = new_array


class Pattern(HasTraits):

    repeat_x = Int

    repeat_y = Int

    array = Array

    def _array_default(self):
        return np.array([[False, True], [True, False], [True, True]])
