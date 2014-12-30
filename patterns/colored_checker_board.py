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

        mapped = model.screen_to_color_index(x, y)
        if mapped is not None:
            index, is_horizontal = mapped
            component.select_color(index, is_horizontal)


class ColoredCheckerBoardComponent(CheckerBoardComponent):

    def _draw(self, gc, view_bounds=None, mode="default"):
        self._draw_color_bars(gc)
        self._draw_colors(gc)
        self._draw_outline(gc)

    def _draw_color_bars(self, gc):

        model = self.model
        x_coords = model._x_coords
        y_coords = model._y_coords
        top, bottom, left, right = model._padding_abs

        with gc:
            gc.set_line_width(2.0)
            gc.set_stroke_color((0.0, 0.0, 0.0))

            for x in x_coords:
                # Vertical strokes
                gc.move_to(x, bottom)
                gc.line_to(x, bottom - 15)
                gc.stroke_path()

            # Top and bottom line
            gc.move_to(x_coords[0], bottom - 15)
            gc.line_to(x_coords[-1], bottom - 15)
            gc.stroke_path()

            for y in y_coords:
                # Horizontal strokes
                gc.move_to(left, y)
                gc.line_to(left - 15, y)
                gc.stroke_path()

            # Left-most line
            gc.move_to(left - 15, y_coords[0])
            gc.line_to(left - 15, y_coords[-1])
            gc.stroke_path()

    def _draw_colors(self, gc):

        model = self.model
        ny, nx = model.data.shape
        x_coords = model._x_coords
        y_coords = model._y_coords
        cx, cy = model._cell_size
        top, bottom, left, right = model._padding_abs

        with gc:
            # Horizontal color bar.
            for x, color in zip(x_coords, model.hor_colors):
                gc.set_fill_color(color)
                gc.draw_rect((x, bottom - 15, cx, 15), FILL)

            # Vertical color bar.
            for y, color in zip(y_coords, model.ver_colors[::-1]):
                gc.set_fill_color(color)
                gc.draw_rect((left - 15, y, 15, cy), FILL)

            # Colors in the interior.
            for i in xrange(nx):
                for j in xrange(ny):
                    if model.data[ny - j - 1, i]:  # Dotted square.
                        color = model.hor_colors[i]
                    else:
                        color = model.ver_colors[ny - j - 1]

                    gc.set_fill_color(color)
                    gc.draw_rect(
                        (x_coords[i], y_coords[j], cx, cy),
                        FILL
                    )

    def select_color(self, index, is_horizontal):
        """
        Display a color dialog box to select a new color.

        """
        if is_horizontal:
            color_array = self.model.hor_colors
        else:
            color_array = self.model.ver_colors
            # Colors are laid out from top to bottom.
            # index = len(color_array) - index - 1

        color = QtGui.QColorDialog.getColor()
        if color.isValid():
            rgb_color = rgb_from_qt_color(color)
            color_array[index] = rgb_color
            print "Selected color {} for box {}.".format(
                rgb_color, (index, is_horizontal))
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
