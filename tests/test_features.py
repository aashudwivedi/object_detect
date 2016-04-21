import numpy as np
import unittest

from voilajones import integral_image


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_integral_image(self):
        ones = np.ones((3,3))
        expected = np.array([
            [1, 2, 3],
            [2, 4, 6],
            [3, 6, 9],
        ])
        returned = integral_image.get_integral_image(ones)
        assert returned == expected
