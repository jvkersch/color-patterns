import numpy as np

from traits.api import Array, HasTraits, Int


class BindingModel(HasTraits):

    rows = Int

    columns = Int

    array = Array

    def _array_default(self):
        return np.array([[False, True], [True, False], [True, True]])

    def _rows_default(self):
        return self.array.shape[0]

    def _columns_default(self):
        return self.array.shape[1]


class PatternRepeatModel(HasTraits):

    repeat_x = Int

    repeat_y = Int


class PatternModel(HasTraits):

    array = Array

    def _array_default(self):
        return np.array([[False, True], [True, False], [True, True]])
