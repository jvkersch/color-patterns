from math import floor
import numpy as np

from traits.api import Array, on_trait_change

from .checker_board_model import CheckerBoardModel


COLOR_DTYPE = np.dtype([('red', float), ('green', float), ('blue', float)])


class ColoredCheckerBoardModel(CheckerBoardModel):

    hor_colors = Array

    ver_colors = Array

    def _hor_colors_default(self):
        arr = np.empty(self.data.shape[1], dtype=COLOR_DTYPE)
        arr.fill((1.0, 1.0, 1.0))
        return arr

    def _ver_colors_default(self):
        arr = np.empty(self.data.shape[0], dtype=COLOR_DTYPE)
        arr.fill((1.0, 1.0, 1.0))
        return arr

    @on_trait_change('data')
    def _update_colors_shape(self):

        # Horizontal colors
        l = min(self.hor_colors.shape[0], self.data.shape[1])
        new = np.empty(self.data.shape[1], dtype=COLOR_DTYPE)
        new.fill((1.0, 1.0, 1.0))
        new[:l] = self.hor_colors[:l]
        self.hor_colors = new

        # Vertical colors
        l = min(self.ver_colors.shape[0], self.data.shape[0])
        new = np.empty(self.data.shape[0], dtype=COLOR_DTYPE)
        new.fill((1.0, 1.0, 1.0))
        new[:l] = self.ver_colors[:l]
        self.ver_colors = new

    def screen_to_color_index(self, x, y):
        """ Translate (x, y) to an index in one of the color arrays.

        Returns
        -------
        index, is_horizontal or None.

        """
        ny, nx = self.data.shape
        cx, cy = self._cell_size
        _, bottom, left, _ = self._padding_abs

        i = int(floor((x - left) / cx))
        j = int(ny - 1 - floor((y - bottom) / cy))

        if j == ny:
            if 0 <= i < nx:
                return i, True
        elif i == -1:
            if 0 <= j < ny:
                return j, False
