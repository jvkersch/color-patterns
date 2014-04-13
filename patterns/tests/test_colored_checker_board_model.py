import unittest
import numpy as np

from traits.testing.unittest_tools import UnittestTools

from ..colored_checker_board_model import ColoredCheckerBoardModel


class TestColoredCheckerBoardModel(unittest.TestCase, UnittestTools):

    def test_initialize(self):

        model = ColoredCheckerBoardModel(data=np.zeros((3, 4)))
        colors = model.colors

        self.assertEqual(colors.shape, (3, 4))
        for entry in colors.flat:
            self.assertSequenceEqual(entry, (1.0, 1.0, 1.0))

    def test_update(self):
        model = ColoredCheckerBoardModel(data=np.zeros((3, 4)))
        colors = model.colors
        colors.fill((0.5, 0.5, 0.5))

        # Enlarge data array.
        with self.assertTraitChanges(model, 'colors', count=1) as ctx:
            model.data = np.zeros((4, 5))

        new_colors = ctx.events[0][-1]
        self.assertEqual(new_colors.shape, (4, 5))

        for entry in new_colors[:3, :4].flat:
            self.assertSequenceEqual(entry, (0.5, 0.5, 0.5))
        for entry in new_colors[3, :].flat:
            self.assertSequenceEqual(entry, (1.0, 1.0, 1.0))
        for entry in new_colors[:, 4].flat:
            self.assertSequenceEqual(entry, (1.0, 1.0, 1.0))

        # Reduce data array.
        with self.assertTraitChanges(model, 'colors', count=1) as ctx:
            model.data = np.zeros((1, 1))

        new_colors = ctx.events[0][-1]
        self.assertEqual(new_colors.shape, (1, 1))
        self.assertSequenceEqual(new_colors[0, 0], (0.5, 0.5, 0.5))


if __name__ == '__main__':
    unittest.main()
