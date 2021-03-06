import numpy as np

from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

from traits.api import Bool, Button, HasTraits, Instance, Int, on_trait_change
from traitsui.api import Group, HGroup, Item, VGroup, View

from pyface.qt import QtGui

from patterns.checker_board import CheckerBoardEditor
from patterns.checker_board_model import CheckerBoardModel
from patterns.colored_checker_board import ColoredCheckerBoardEditor
from patterns.colored_checker_board_model import (
    ColoredCheckerBoardModel
)
from patterns.io import load_models, save_models


class MainWindow(HasTraits):

    binding = Instance(CheckerBoardModel)

    binding_rows = Int(2)

    binding_cols = Int(2)

    pattern = Instance(ColoredCheckerBoardModel)

    pattern_repeat_x = Int(4)

    pattern_repeat_y = Int(4)

    # UI elements
    save = Button('Save...')
    load = Button('Open...')

    view = View(
        VGroup(
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
                    ),
                ),
                Group(
                    Item('pattern', editor=ColoredCheckerBoardEditor()),
                    show_border=True,
                    show_labels=False,
                    label='Pattern'),
            ),
            HGroup(
                Item("save", show_label=False),
                Item("load", show_label=False),
            )
        ),
        title='Color Patterns',
    )

    # Loopback guard to prevent cyclic updates between pattern and binding.
    _update_binding = Bool(False)

    def _binding_default(self):
        data = np.zeros((self.binding_rows, self.binding_cols), dtype=bool)
        return CheckerBoardModel(data=data)

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

    @on_trait_change(
        'binding_cols, binding_rows, binding:[data_updated, size_changed]')
    def _update_pattern_data(self):
        self._update_binding = True
        try:
            # Simply replicate the pattern everywhere.
            self.pattern.data = np.tile(
                self.binding.data,
                (self.pattern_repeat_y, self.pattern_repeat_x)
            )
            self.pattern.data_updated = True
        finally:
            self._update_binding = False

    @on_trait_change('pattern:data_updated')
    def _update_binding_data(self):
        if self._update_binding:
            return  # Binding already updated.

        rows = self.binding_rows
        cols = self.binding_cols
        self.binding.data = self.pattern.data[:rows, :cols]
        self.binding.data_updated = True

    def _load_changed(self):
        filename = QtGui.QFileDialog.getOpenFileName()[0]
        if filename != '':
            print 'Loading from', filename
            load_models(filename, self)

    def _save_changed(self):
        filename = QtGui.QFileDialog.getSaveFileName()[0]
        if filename != '':
            print 'Saving to', filename
            save_models(filename, self)


def main():
    main_window = MainWindow()
    main_window.configure_traits()


if __name__ == '__main__':
    main()
