from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

from traitsui.api import Group, HGroup, Item, VGroup, View

from patterns.checker_board import CheckerBoardEditor
from patterns.colored_checker_board import ColoredCheckerBoardEditor

from patterns.models import BindingModel, PatternModel, PatternRepeatModel


view = View(
    HGroup(
        VGroup(
            VGroup(
                Item('binding.rows'),
                Item('binding.columns'),
                Item(
                    'binding.array',
                    editor=CheckerBoardEditor(),
                    label='Binding'),
                Item('repeat.repeat_x'),
                Item('repeat.repeat_y'),
                label='Binding',
                show_border=True,
            )
        ),
        Group(
            Item('pattern.array', editor=ColoredCheckerBoardEditor()),
            show_border=True,
            show_labels=False,
            label='Pattern'),
        )
    )


if __name__ == '__main__':

    binding = BindingModel()
    pattern = PatternModel()
    repeat = PatternRepeatModel()

    binding.configure_traits(
        view=view,
        context={'binding': binding, 'pattern': pattern, 'repeat': repeat}
    )
