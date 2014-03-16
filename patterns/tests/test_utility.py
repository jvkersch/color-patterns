import unittest

from ..utility import rgb_from_qt_color


class DummyQColor(object):

    def __init__(self, colors):
        self.colors = colors

    def red(self):
        return self.colors[0]

    def green(self):
        return self.colors[1]

    def blue(self):
        return self.colors[2]


class RGBTestCase(unittest.TestCase):

    def _check_colors(self, testcases):

        for fvals, ivals in testcases.iteritems():
            color = DummyQColor(fvals)
            rgb = rgb_from_qt_color(color)
            self.assertSequenceEqual(rgb, ivals)

    def test_extremes(self):

        testcases = {
            (0.0, 0.0, 0.0): (0, 0, 0),
            (1.0, 1.0, 1.0): (255, 255, 255),
            (0.0, 1.0, 0.0): (0, 255, 0)
        }
        self._check_colors(testcases)

    def test_colors(self):

        testcases = {
            (0.1, 0.2, 0.3) : (25, 51, 76)
        }
        self._check_colors(testcases)


if __name__ == '__main__':
    unittest.main()
