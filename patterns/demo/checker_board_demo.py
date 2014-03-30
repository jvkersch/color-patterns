"""
Simple pattern editor example.

"""

import numpy as np

from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

from traits.api import HasTraits, Instance
from traitsui.api import Item, View

from patterns.checker_board import CheckerBoardEditor
from patterns.checker_board_model import CheckerBoardModel


class MainWindow(HasTraits):

    board = Instance(CheckerBoardModel)

    view = View(
        Item('board', editor=CheckerBoardEditor()),
        resizable=True
    )

    def _board_default(self):
        data = np.array([[False, True], [True, False], [True, True]])
        return CheckerBoardModel(data=data)


if __name__ == '__main__':
    main = MainWindow()
    main.configure_traits()
