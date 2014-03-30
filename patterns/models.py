"""
Simple facades around checkerboard models, adapted for various purposes.


"""

import numpy as np

from traits.api import Array, HasTraits, Int


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


class Pattern(HasTraits):

    repeat_x = Int

    repeat_y = Int

    array = Array

    def _array_default(self):
        return np.array([[False, True], [True, False], [True, True]])
