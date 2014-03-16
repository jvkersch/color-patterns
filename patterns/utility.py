from fractions import gcd as standard_gcd


def gcd(a, b):
    """ Returns the greatest common divisor of the two given numbers.
    """
    return standard_gcd(a, b)

def lcm(a, b):
    """ Returns the least common multiple of the two given numbers.
    """
    return a * b / standard_gcd(a, b)

def rgb_from_qt_color(color):
    """
    Convert a QColor instance into an (R, G, B) tuple.

    For a valid QColor, the color components are integers in
    the range 0..255.

    """
    return tuple(int(255 * c) for c in (
        color.red(), color.green(), color.blue()))
