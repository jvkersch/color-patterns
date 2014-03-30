from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

from traitsui.api import Group, HGroup, Item, VGroup, View

from patterns.checker_board import CheckerBoardEditor
from patterns.colored_checker_board import ColoredCheckerBoardEditor

from patterns.models import Binding, Pattern, PatternController


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
                Item('pattern.repeat_x'),
                Item('pattern.repeat_y'),
                label='Binding',
                show_border=True,
            )
        ),
        Group(
            Item('pattern.array', editor=ColoredCheckerBoardEditor()),
            show_border=True,
            show_labels=False,
            label='Pattern'),
        ),
    title='Color Patterns',
)


if __name__ == '__main__':

    controller = PatternController()
    binding = controller.binding
    pattern = controller.pattern

    binding.configure_traits(
        view=view,
        context={'binding': binding, 'pattern': pattern}
    )
