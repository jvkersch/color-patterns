"""
Simple pattern editor example.

"""

import numpy as np

from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

from traits.api import HasTraits, Instance
from traitsui.api import Item, View

from patterns.colored_checker_board import ColoredCheckerBoardEditor
from patterns.colored_checker_board_model import (
    ColoredCheckerBoardModel
)


class MainWindow(HasTraits):

    board = Instance(ColoredCheckerBoardModel)

    view = View(
        Item('board', editor=ColoredCheckerBoardEditor()),
        resizable=True
    )

    def _board_default(self):
        data = np.array([[False, True], [True, False], [True, True]])
        return ColoredCheckerBoardModel(data=data)


if __name__ == '__main__':
    main = MainWindow()
    main.configure_traits()
