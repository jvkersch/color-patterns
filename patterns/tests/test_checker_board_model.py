import unittest

import numpy as np

from ..checker_board_model import CheckerBoardModel


class TestCheckerBoardModel(unittest.TestCase):

    def test_hits(self):

        data = np.array([[True, False], [False, True], [False, False]])

        model = CheckerBoardModel(
            data=data,
            padding=(0.1, 0.2, 0.3, 0.35),
            size=(139, 267),
        )
        sx, sy = model.size

        top, bottom, left, right = model._padding_abs
        hits = model.is_inside

        for point in ((left - 1, bottom),
                       (left, sy - top + 1),
                       (left, bottom - 1),
                       (sx - right + 1, bottom),
                       (sx - right - 1, bottom - 1),
                       (sx - right - 1, sy - top + 1)):

            self.assertFalse(hits(*point))

        for point in ((left + 1, bottom + 1),
                      (left + 1, sy / 2),
                      (left + 1, sy - top - 1),
                      (sx / 2, sy - top - 1),
                      (sx / 2, bottom + 1),
                      (sx - right - 1, bottom + 1),
                      (sx - right - 1, sy / 2),
                      (sx - right - 1, sy - top - 1)):

            self.assertTrue(hits(*point))

    def test_screen_to_array_index(self):

        data = np.array([[True, False, True], [False, True, False]])
        model = CheckerBoardModel(
            data=data,
            padding=(0.1, 0.2, 0.15, 0.25),
            size=(200, 100),
        )

        to_array = model.screen_to_array_index

        cx, cy = model._cell_size
        _, bottom, left, _ = model._padding_abs

        for i in range(3):
            for j in range(2):
                x = left + cx * (2 * i + 1) / 2
                y = bottom + cy * (2 * j + 1) / 2
                self.assertEqual(to_array(x, y), (1 - j, i))

        with self.assertRaises(ValueError):
            to_array(*model.size)  # A point outside the board.

    # def test_cell_center(self):

    #     data = np.array([[True, False], [False, True], [False, False]])
    #     model = CheckerBoardModel(
    #         data=data,
    #         padding=(3, 7),
    #         cell_size=(10, 20),
    #     )

    #     ctr = model.cell_center

    #     # Comparison with precomputed values.
    #     self.assertEqual(ctr(0, 0), (8, 57))
    #     self.assertEqual(ctr(0, 1), (18, 57))
    #     self.assertEqual(ctr(1, 0), (8, 37))
    #     self.assertEqual(ctr(1, 2), (28, 37))

    #     # Round-trip test.
    #     to_array = model.screen_to_array_index
    #     for i in xrange(data.shape[0]):
    #         for j in xrange(data.shape[1]):
    #             point = ctr(i, j)
    #             self.assertEqual(to_array(*point), (i, j))