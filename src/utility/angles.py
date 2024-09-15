#!/usr/bin/env python3

import math
import unittest

def wrap_angle(angle):
    """
    Wraps the given angle between -pi and pi.
    
    Parameters:
        angle (float): The angle in radians to be wrapped.
    
    Returns:
        float: The angle wrapped to the range [-pi, pi].
    """
    pi = math.pi
    angle = math.fmod(angle, 2 * pi)
    if angle >= pi:
        angle -= 2 * pi
    elif angle < -pi:
        angle += 2 * pi
    return angle

class TestWrapAngle(unittest.TestCase):

    def test_positive_wrap(self):
        self.assertAlmostEqual(wrap_angle(math.pi + 0.1), -math.pi + 0.1)
    
    def test_negative_wrap(self):
        self.assertAlmostEqual(wrap_angle(-math.pi - 0.1), math.pi - 0.1)
    
    def test_no_wrap_required(self):
        self.assertAlmostEqual(wrap_angle(math.pi / 2), math.pi / 2)
    
    def test_full_rotation(self):
        self.assertAlmostEqual(wrap_angle(2 * math.pi), 0)
    
    def test_full_negative_rotation(self):
        self.assertAlmostEqual(wrap_angle(-2 * math.pi), 0)

    def test_over_two_rotations(self):
        self.assertAlmostEqual(wrap_angle(4 * math.pi + 1), 1)

    def test_under_two_negative_rotations(self):
        self.assertAlmostEqual(wrap_angle(-4 * math.pi - 1), -1)

    def test_wrap(self):
        self.assertAlmostEqual(wrap_angle(math.pi + .1), -math.pi + .1)

if __name__ == '__main__':
    unittest.main()
