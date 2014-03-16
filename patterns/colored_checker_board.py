from enable.api import BaseTool, ColorTrait

from .checker_board import (
    CheckerBoardComponent, _CheckerBoardEditor,
    CheckerBoardEditor, ToggleClickerTool
)
from .colored_checker_board_model import ColoredCheckerBoardModel


class RightClickerTool(BaseTool):

    def normal_right_down(self, event):

        x = event.x
        y = event.y

        component = self.component
        model = component.model

        try:
            mapped_index = model.screen_to_array_index(x, y)
        except ValueError:
            pass
        else:
            print "Right click on", mapped_index


class ColoredCheckerBoardComponent(CheckerBoardComponent):

    def _tools_default(self):
        return [RightClickerTool(self), ToggleClickerTool(self)]


class _ColoredCheckerBoardEditor(_CheckerBoardEditor):

    def _make_component(self, arr):
        component = ColoredCheckerBoardComponent(
            model=ColoredCheckerBoardModel(data=arr)
        )
        component.request_redraw()
        return component


class ColoredCheckerBoardEditor(CheckerBoardEditor):

    klass = _ColoredCheckerBoardEditor

    bgcolor = ColorTrait('sys_window')
