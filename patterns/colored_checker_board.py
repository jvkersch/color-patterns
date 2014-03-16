from enable.api import BaseTool, ColorTrait
from pyface.qt import QtGui

from .checker_board import (
    CheckerBoardComponent, _CheckerBoardEditor,
    CheckerBoardEditor, ToggleClickerTool
)
from .colored_checker_board_model import ColoredCheckerBoardModel
from .utility import rgb_from_qt_color


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
            component.select_color(*mapped_index)


class ColoredCheckerBoardComponent(CheckerBoardComponent):

    def _draw(self, gc, view_bounds=None, mode="default"):

        self._draw_colors(gc)
        self._draw_outline(gc)

    def _draw_colors(self, gc):
        pass

    def select_color(self, i, j):
        """
        Display a color dialog box to select a color for square (i, j).

        """
        color = QtGui.QColorDialog.getColor()
        if color.isValid():
            print "selected", rgb_from_qt_color(color)

    def _tools_default(self):
        return [RightClickerTool(self), ToggleClickerTool(self)]


class _ColoredCheckerBoardEditor(_CheckerBoardEditor):

    def _make_component(self, arr):

        component = ColoredCheckerBoardComponent(
            model=ColoredCheckerBoardModel(data=arr)
        )
        component.request_redraw()
        return component

    def dispose ( self ):

        super(_ColoredCheckerBoardEditor, self).dispose()


class ColoredCheckerBoardEditor(CheckerBoardEditor):

    klass = _ColoredCheckerBoardEditor

    bgcolor = ColorTrait('sys_window')
