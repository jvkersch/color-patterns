from math import floor, pi

from enable.api import BaseTool, ColorTrait, Component, Window
from traits.api import Array, DelegatesTo, Instance, on_trait_change
from traitsui.qt4.editor import Editor
from traitsui.qt4.basic_editor_factory import BasicEditorFactory

from .checker_board_model import CheckerBoardModel


class ToggleClickerTool(BaseTool):

    def normal_left_down(self, event):
        x = event.x
        y = event.y
        component = self.component

        print 'Clicked on', x, y

        mapped_index = component._pixel_coordinates_to_index(x, y)
        if mapped_index is not None:  # TODO have a is_inside method on the model.
            i, j = mapped_index
            print i, j
            component._toggle_value(i, j)
            component.request_redraw()


class CheckerBoardComponent(Component):

    model = Instance(CheckerBoardModel)

    data = DelegatesTo('model')

    padding = DelegatesTo('model')

    def _draw(self, gc, view_bounds=None, mode="default"):

        model = self.model
        model.size = tuple(self.bounds)

        # Make this into a property.
        abs_size_x, abs_size_y = model._cell_size
        abs_radius = max(0.10 * min(abs_size_x, abs_size_y), 3.0)

        x_coords = model._x_coords
        y_coords = model._y_coords

        top, bottom, left, right = model._padding_abs
        sx, sy = model.size

        ny, nx = model.data.shape

        with gc:
            gc.set_line_width(2.0)
            gc.set_stroke_color((0.0, 0.0, 0.0))

            for x in x_coords:
                # Vertical lines.
                gc.move_to(x, bottom)
                gc.line_to(x, sy - top)
                gc.stroke_path()

            for y in y_coords:
                # Horizontal lines.
                gc.move_to(left, y)
                gc.line_to(sx - right, y)
                gc.stroke_path()

            for i in range(nx):
                for j in range(ny):
                    if model.data[j, i]:
                        center = model.cell_center(i, j)
                        gc.arc(center[0], center[1], abs_radius, 0, 2 * pi)
                        gc.fill_path()

    # def _pixel_coordinates_to_index(self, x, y):
    #     # TODO Should this be part of the model?

    #     # TODO: refactor this. This is an exact duplicate of the calculations
    #     # above.
    #     t_array = self.array.T

    #     dx, dy = self.bounds

    #     nr_x_boxes, nr_y_boxes = t_array.shape

    #     rel_size = 0.2
    #     abs_size_x = rel_size * dx
    #     abs_size_y = rel_size * dy

    #     abs_radius = max(0.10 * min(abs_size_x, abs_size_y), 3.0)

    #     padding_x = (1.0 - rel_size * nr_x_boxes) * dx / 2.0
    #     padding_y = (1.0 - rel_size * nr_y_boxes) * dy / 2.0

    #     x_coords = [padding_x + k * abs_size_x for k in xrange(nr_x_boxes + 1)]
    #     y_coords = [padding_y + k * abs_size_y for k in xrange(nr_y_boxes + 1)]

    #     if x < x_coords[0] or x > x_coords[-1]:
    #         return None
    #     if y < y_coords[0] or y > y_coords[-1]:
    #         return None

    #     x -= padding_x
    #     y -= padding_y

    #     i = floor(x / abs_size_x)
    #     j = floor(y / abs_size_y)

    #     j = nr_y_boxes - 1 - j

    #     return int(j), int(i)

    # def _toggle_value(self, i, j):

    #     self.array[i, j] = not self.array[i, j]

        


class _CheckerBoardEditor(Editor):

    scrollable = True

    def init(self, parent):
        component = self._make_component(self.value)
        self._window = Window(parent, size=(200, 200), component=component)
        self.control = self._window.control
        self._window.bgcolor = self.factory.bgcolor
        self._parent = parent

    def dispose(self):
        self._window.cleanup()
        self._window = None
        self._parent = None
        super(_CheckerBoardEditor, self).dispose()

    def update_editor(self):
        component = self._make_component(self.value)
        self._window.component = component

    def _make_component(self, arr):
        print 'Making new component'
        component = CheckerBoardComponent(
            model=CheckerBoardModel(data=self.value)
        )
        component.request_redraw()
        return component


class CheckerBoardEditor(BasicEditorFactory):

    klass = _CheckerBoardEditor

    bgcolor = ColorTrait('sys_window')
