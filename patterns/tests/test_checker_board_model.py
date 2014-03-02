import unittest

import numpy as np

from ..checker_board_model import CheckerBoardModel


class TestCheckerBoardModel(unittest.TestCase):

    def test_properties(self):

        data = np.array([[True, False], [False, True], [False, False]])
        model = CheckerBoardModel(
            data=data,
            padding=(10, 10),
            cell_size=(20, 20),
        )

        precomputed_size = (60, 80)
        self.assertEqual(model.size, precomputed_size)

        model.padding = (0, 0)
        precomputed_size = (40, 60)
        self.assertEqual(model.size, precomputed_size)

    def test_hits(self):

        data = np.array([[True, False], [False, True], [False, False]])

        px, py = (5, 10)
        model = CheckerBoardModel(
            data=data,
            padding=(px, py),
            cell_size=(15, 20),
        )

        sx, sy = model.size

        hits = model.is_inside
        self.assertFalse(hits(px / 2, sy / 2))
        self.assertFalse(hits(sx / 2, py / 2))
        self.assertTrue(hits(sx / 2, sy / 2))
        self.assertFalse(hits(sx - px / 2, sy / 2))
        self.assertFalse(hits(sx / 2, sy - py / 2))

    def test_screen_to_array_index(self):

        data = np.array([[True, False], [False, True], [False, False]])
        model = CheckerBoardModel(
            data=data,
            padding=(0, 0),
            cell_size=(10, 20),
        )

        to_array = model.screen_to_array_index

        # Array layout for the next set of assertions:
        # [. .]
        # [3 .]
        # [1 2]
        self.assertEqual(to_array(5, 10), (2, 0))  # 1
        self.assertEqual(to_array(15, 10), (2, 1))  # 2
        self.assertEqual(to_array(5, 30), (1, 0))  # 3

        with self.assertRaises(ValueError):
            to_array(200, 200)  # A point outside the board.

    def test_cell_center(self):

        data = np.array([[True, False], [False, True], [False, False]])
        model = CheckerBoardModel(
            data=data,
            padding=(3, 7),
            cell_size=(10, 20),
        )

        ctr = model.cell_center

        # Comparison with precomputed values.
        self.assertEqual(ctr(0, 0), (8, 57))
        self.assertEqual(ctr(0, 1), (18, 57))
        self.assertEqual(ctr(1, 0), (8, 37))
        self.assertEqual(ctr(1, 2), (28, 37))

        # Round-trip test.
        to_array = model.screen_to_array_index
        for i in xrange(data.shape[0]):
            for j in xrange(data.shape[1]):
                point = ctr(i, j)
                self.assertEqual(to_array(*point), (i, j))
