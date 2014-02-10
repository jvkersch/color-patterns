import unittest

import numpy as np
from numpy.testing import assert_array_equal

from ..pattern import Pattern


COLORS = [
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0],
    [0.0, 1.0, 1.0],
    [1.0, 0.0, 1.0],
    [1.0, 1.0, 0.0],
    [1.0, 1.0, 1.0],
    [0.0, 0.0, 0.0]
]


class TestPattern(unittest.TestCase):

    def test_simple_pattern(self):
        binding = np.array([[True, False], [False, True]])
        x_colors = np.array(COLORS[:3])
        y_colors = np.array(COLORS[3:])

        p = Pattern(
            binding=binding, x_colors=x_colors, y_colors=y_colors)

        p_data = p.pattern
        self.assertEqual(p_data.shape, (6, 10, 3))

        # Manually check colors.
        for i in range(6):
            for j in range(10):
                if binding[i % 2, j % 2]:
                    assert_array_equal(p_data[i, j, :], x_colors[i % 3])
                else:
                    assert_array_equal(p_data[i, j, :], y_colors[j % 5])
