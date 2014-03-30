from fractions import gcd as standard_gcd


def gcd(a, b):
    """ Returns the greatest common divisor of the two given numbers.
    """
    return standard_gcd(a, b)


def lcm(a, b):
    """ Returns the least common multiple of the two given numbers.
    """
    return a * b / standard_gcd(a, b)
