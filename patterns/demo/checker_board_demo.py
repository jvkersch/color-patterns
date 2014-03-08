"""
Simple pattern editor example.

"""

import numpy as np

from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

from traits.api import Array, HasTraits
from traitsui.api import Item, View

from patterns.checker_board import CheckerBoardEditor


class MainWindow(HasTraits):

    array = Array

    view = View(
        Item('array', editor=CheckerBoardEditor()),
        resizable=True
    )

    def _array_default(self):
        return np.array([[False, True], [True, False], [True, True]])


if __name__ == '__main__':
    main = MainWindow()
    main.configure_traits()
