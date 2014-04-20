from enable.api import BaseTool, ColorTrait
from kiva.constants import FILL

from pyface.qt import QtGui

from .checker_board import (
    CheckerBoardComponent, _CheckerBoardEditor, CheckerBoardEditor
)


def rgb_from_qt_color(color):

    return (color.red() / 255.0, color.green() / 255.0, color.blue() / 255.0)


class ColorSelectTool(BaseTool):

    def normal_left_down(self, event):

        x = event.x
        y = event.y

        component = self.component
        model = component.model

        try:
            mapped_index = model.screen_to_array_index(x, y)
        except ValueError:
            pass
        else:
            component.select_color(*mapped_index)


class ColoredCheckerBoardComponent(CheckerBoardComponent):

    def _draw(self, gc, view_bounds=None, mode="default"):

        self._draw_colors(gc)
        self._draw_outline(gc)

    def _draw_colors(self, gc):

        model = self.model
        ny, nx = model.data.shape
        x_coords = model._x_coords
        y_coords = model._y_coords
        cx, cy = model._cell_size

        with gc:
            for i in range(nx):
                for j in range(ny):
                    color = self.model.colors[ny - 1 - j, i]
                    gc.set_fill_color(color)
                    gc.draw_rect(
                        (x_coords[i], y_coords[j], cx, cy),
                        FILL)

    def select_color(self, i, j):
        """
        Display a color dialog box to select a color for square (i, j).

        """
        color = QtGui.QColorDialog.getColor()
        if color.isValid():
            rgb_color = rgb_from_qt_color(color)
            self.model.colors[i, j] = rgb_color
            print "Selected color {} for box {}.".format(
                rgb_color, (i, j))
            self.request_redraw()

    def _tools_default(self):
        return [ColorSelectTool(self)]


class _ColoredCheckerBoardEditor(_CheckerBoardEditor):

    def _make_component(self, model):
        component = ColoredCheckerBoardComponent(model=model)
        component.request_redraw()
        return component


class ColoredCheckerBoardEditor(CheckerBoardEditor):

    klass = _ColoredCheckerBoardEditor

    bgcolor = ColorTrait('sys_window')
