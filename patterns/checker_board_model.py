from math import floor

import numpy as np

from traits.api import (
    Array, Event, Float, HasTraits, Int, List, Property, Tuple)


class CheckerBoardModel(HasTraits):
    """
    A checker board pattern with a fixed screen width and height.

    """
    # Event fired when the checkerboard data has been updated.
    updated = Event

    # Array specifying the checkerboard pattern.
    data = Array

    # Rows on the checkerboard.
    rows = Property(Int)

    # Columns on the checkerboard.
    columns = Property(Int)

    # Padding to add to the board (in relative coordinates, along
    # (top, bottom, left, right)).
    padding = Tuple(Float, Float, Float, Float)

    # Total size of the board (in pixels).
    size = Tuple(Int, Int)

    # Padding in absolute coordinates.
    _padding_abs = Property(Tuple(Int, Int, Int, Int))

    # Size of the individual cells of the board (in pixels).
    _cell_size = Property(Tuple(Int, Int))

    # x-coordinates of the checkerboard pattern lines.
    _x_coords = Property(List(Int))

    # y-coordinates of the checkerboard pattern lines.
    _y_coords = Property(List(Int))

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value
        self.updated = True

    def is_inside(self, x, y):
        """ Checks whether the point with coordinates `(x, y)` is inside
        the checkerboard.

        """
        top, bottom, left, right = self._padding_abs
        sx, sy = self.size
        return all((x > left, x < sx - right, y > bottom, y < sy - top))

    def screen_to_array_index(self, x, y):
        """ Returns the array index corresponding to a point inside
        the checkerboard.

        Raises
        ------
        ValueError
            If the point is outside the checkerboard.

        """

        if not self.is_inside(x, y):
            msg = 'Point with coordinates {} is outside checkerboard.'
            raise ValueError(msg.format((x, y)))

        ny = self.data.shape[0]
        cx, cy = self._cell_size
        _, bottom, left, _ = self._padding_abs

        i = int(floor((x - left) / cx))
        j = int(ny - 1 - floor((y - bottom) / cy))

        return j, i

    def cell_center(self, i, j):
        """ Returns the coordinates of the center of the cell with logical
        index `(i, j)`.

        """
        ny, _ = self.data.shape
        cx, cy = self._cell_size
        center_x = self._x_coords[j] + cx / 2
        center_y = self._y_coords[ny - i - 1] + cy / 2
        return (center_x, center_y)

    def _padding_default(self):
        return (0.1, 0.1, 0.1, 0.1)

    def _get__padding_abs(self):

        top, bottom, left, right = self.padding
        sx, sy = self.size
        return (
            int(sy * top), int(sy * bottom), int(sx * left), int(sx * right)
        )

    def _get__cell_size(self):

        top, bottom, left, right = self._padding_abs
        sx, sy = self.size
        ny, nx = self.data.shape
        return ((sx - left - right) / nx, (sy - top - bottom) / ny)

    def _get__x_coords(self):
        """ Get the x-coordinates of the vertical checkerboard grid lines.
        """
        _, nx = self.data.shape
        cx, _ = self._cell_size
        left = self._padding_abs[2]
        return [left + k * cx for k in xrange(nx + 1)]

    def _get__y_coords(self):
        """ Get the y-coordinates of the horizontal checkerboard grid lines.
        """
        ny, _ = self.data.shape
        _, cy = self._cell_size
        bottom = self._padding_abs[1]
        return [bottom + k * cy for k in xrange(ny + 1)]

    def _get_rows(self):
        return self.data.shape[0]

    def _get_columns(self):
        return self.data.shape[1]

    def _set_rows(self, value):
        self.reshape_data((value, self.columns))

    def _set_columns(self, value):
        self.reshape_data((self.rows, value))

    def reshape_data(self, new_shape):
        """ Adjust the data array to the new shape.
        """
        # TODO There is probably a Numpy function that does this already.
        new_array = np.zeros(new_shape, dtype=bool)
        old_rows, old_columns = self.data.shape
        rows = min(old_rows, new_shape[0])
        columns = min(old_columns, new_shape[1])
        new_array[:rows, :columns] = self.data[:rows, :columns]

        self.data = new_array
        self.updated = True
