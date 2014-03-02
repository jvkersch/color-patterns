from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

from enable.colors import ColorTrait
from enable.api import Component, Window

from traits.api import Array

from traitsui.qt4.editor import Editor
from traitsui.qt4.basic_editor_factory import BasicEditorFactory


class CheckerBoardComponent(Component):

    array = Array

    def _draw(self, gc, view_bounds=None, mode="default"):

        t_array = self.array.T

        dx, dy = self.bounds
        x, y = self.position

        nr_x_boxes, nr_y_boxes = t_array.shape

        rel_size = 0.2
        abs_size_x = rel_size * dx
        abs_size_y = rel_size * dy

        abs_radius = max(0.10 * min(abs_size_x, abs_size_y), 3.0)

        padding_x = (1.0 - rel_size * nr_x_boxes) * dx / 2.0
        padding_y = (1.0 - rel_size * nr_y_boxes) * dy / 2.0

        x_coords = [padding_x + k * abs_size_x for k in xrange(nr_x_boxes + 1)]
        y_coords = [padding_y + k * abs_size_y for k in xrange(nr_y_boxes + 1)]

        with gc:
            gc.set_line_width(2.0)
            gc.set_stroke_color((0.0, 0.0, 0.0))

            for x in x_coords:
                gc.move_to(x, dy - padding_y)
                gc.line_to(x, padding_y)
                gc.stroke_path()

            for y in y_coords:
                gc.move_to(padding_x, y)
                gc.line_to(dx - padding_x, y)
                gc.stroke_path()

            for i in range(nr_x_boxes):
                for j in range(nr_y_boxes):
                    if t_array[i, j]:
                        cx = x_coords[i] + abs_size_x / 2
                        cy = dy - (y_coords[j] + abs_size_y / 2)
                        gc.arc(cx, cy, abs_radius, 0, 2 * 3.1415)
                        gc.fill_path()


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
        component = CheckerBoardComponent(array=self.value)
        component.request_redraw()
        return component


class CheckerBoardEditor(BasicEditorFactory):

    klass = _CheckerBoardEditor

    bgcolor = ColorTrait('sys_window')
