import numpy as np

from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

from traits.api import HasTraits, Instance, Int, on_trait_change
from traitsui.api import Group, HGroup, Item, VGroup, View

from patterns.checker_board import CheckerBoardEditor
from patterns.checker_board_model import CheckerBoardModel
from patterns.colored_checker_board import ColoredCheckerBoardEditor
from patterns.colored_checker_board_model import (
    ColoredCheckerBoardModel
)


class MainWindow(HasTraits):

    binding = Instance(CheckerBoardModel)

    binding_rows = Int

    binding_cols = Int

    pattern = Instance(ColoredCheckerBoardModel)

    pattern_repeat_x = Int(2)

    pattern_repeat_y = Int(2)

    view = View(
        HGroup(
            VGroup(
                VGroup(
                    Item('binding_rows'),
                    Item('binding_cols'),
                    Item(
                        'binding',
                        editor=CheckerBoardEditor(),
                        label='Binding'),
                    Item('pattern_repeat_x'),
                    Item('pattern_repeat_y'),
                    label='Binding',
                    show_border=True,
                )
            ),
            Group(
                Item('pattern', editor=ColoredCheckerBoardEditor()),
                show_border=True,
                show_labels=False,
                label='Pattern'),
        ),
        title='Color Patterns',
    )

    def _binding_default(self):
        data = np.array([[False, True], [True, False], [True, True]])
        return CheckerBoardModel(data=data)

    def _binding_rows_default(self):
        return self.binding.rows

    def _binding_cols_default(self):
        return self.binding.columns

    def _pattern_default(self):
        cols = self.pattern_repeat_x * self.binding_cols
        rows = self.pattern_repeat_y * self.binding_rows
        data = np.zeros((rows, cols), dtype=bool)
        return ColoredCheckerBoardModel(data=data)

    @on_trait_change('binding_rows')
    def _update_binding_rows(self, value):
        self.binding.rows = value
        self.pattern.rows = value * self.pattern_repeat_y

    @on_trait_change('binding_cols')
    def _update_binding_cols(self, value):
        self.binding.columns = value
        self.pattern.columns = value * self.pattern_repeat_x

    @on_trait_change('pattern_repeat_x')
    def _update_pattern_cols(self, value):
        self.pattern.columns = value * self.binding_cols

    @on_trait_change('pattern_repeat_y')
    def _update_pattern_rows(self, value):
        self.pattern.rows = value * self.binding_rows

    @on_trait_change('binding:data_updated')
    def _update_pattern_data(self, value):
        # Simply replicate the pattern everywhere.
        self.pattern.data = np.tile(
            self.binding.data,
            (self.pattern_repeat_y, self.pattern_repeat_x)
        )
        self.pattern.data_updated = True  # Hmmm.


if __name__ == '__main__':
    main = MainWindow()
    main.configure_traits()
