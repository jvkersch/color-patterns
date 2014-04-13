"""
Simple pattern editor example.

"""

import numpy as np

from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

from traits.api import HasTraits, Instance, Int, on_trait_change
from traitsui.api import HGroup, VGroup, Item, View

from patterns.checker_board import CheckerBoardEditor
from patterns.checker_board_model import CheckerBoardModel


class MainWindow(HasTraits):

    board = Instance(CheckerBoardModel)

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
            Item('board', editor=CheckerBoardEditor()),
        ),
        resizable=True
    )

    def _board_default(self):
        data = np.array([[False, True], [True, False], [True, True]])
        return CheckerBoardModel(data=data)

    def _rows_default(self):
        return self.board.rows

    def _columns_default(self):
        return self.board.columns

    @on_trait_change('rows, columns')
    def _update_array_size(self):
        self.board.columns = self.columns
        self.board.rows = self.rows


if __name__ == '__main__':
    main = MainWindow()
    main.configure_traits()
