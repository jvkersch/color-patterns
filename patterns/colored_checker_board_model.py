import numpy as np

from traits.api import Array, on_trait_change

from .checker_board_model import CheckerBoardModel


COLOR_DTYPE = np.dtype([('red', float), ('green', float), ('blue', float)])


class ColoredCheckerBoardModel(CheckerBoardModel):

    colors = Array

    def _colors_default(self):
        arr = np.empty(self.data.shape, dtype=COLOR_DTYPE)
        arr.fill((1.0, 1.0, 1.0))
        return arr

    @on_trait_change('data')
    def _update_colors_shape(self):

        cx, cy = [min(*t) for t in zip(self.colors.shape, self.data.shape)]
        new_colors = np.empty(self.data.shape, dtype=COLOR_DTYPE)
        new_colors.fill((1.0, 1.0, 1.0))
        new_colors[:cx, :cy] = self.colors[:cx, :cy]
        self.colors = new_colors
