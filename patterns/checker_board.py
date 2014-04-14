from math import pi

from enable.api import BaseTool, ColorTrait, Component, Window
from traits.api import DelegatesTo, Instance, on_trait_change
from traitsui.qt4.editor import Editor
from traitsui.qt4.basic_editor_factory import BasicEditorFactory

from .checker_board_model import CheckerBoardModel


class ToggleClickerTool(BaseTool):

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
            component._toggle_value(*mapped_index)
            component.request_redraw()


class CheckerBoardComponent(Component):

    model = Instance(CheckerBoardModel)

    data = DelegatesTo('model')

    padding = DelegatesTo('model')

    def _draw(self, gc, view_bounds=None, mode="default"):
        self._draw_outline(gc)

    def _draw_outline(self, gc):

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
                        center = model.cell_center(j, i)
                        gc.arc(center[0], center[1], abs_radius, 0, 2 * pi)
                        gc.fill_path()

    def _tools_default(self):
        return [ToggleClickerTool(self)]

    def _toggle_value(self, i, j):
        self.model[i, j] = not self.model[i, j]

    @on_trait_change('model.[data_updated, size_changed]')
    def redraw(self):
        self.request_redraw()


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

    @on_trait_change('value')
    def update_editor(self):
        component = self._make_component(self.value)
        self._window.component = component

    def _make_component(self, model):
        component = CheckerBoardComponent(model=model)
        component.request_redraw()
        return component


class CheckerBoardEditor(BasicEditorFactory):

    klass = _CheckerBoardEditor

    bgcolor = ColorTrait('sys_window')
