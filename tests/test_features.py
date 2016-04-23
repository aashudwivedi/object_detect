import numpy as np
import unittest

from .. import voilajones as vj


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_integral_image(self):
        ones = np.ones((3, 3))
        expected = np.array([
            [1, 2, 3],
            [2, 4, 6],
            [3, 6, 9],
        ])

        returned = vj.features.get_integral_image(ones)

        assert (returned == expected).all(), returned

    def test_area_sum(self):
        ones = np.ones((3, 3))
        integral_image = vj.features.get_integral_image(ones)

        top_left = (0, 0)
        height = 1
        width = 1
        returned = vj.features.get_area_sum(integral_image, top_left,
                                            height, width)
        assert returned == 1.0

        height = 2
        width = 2
        returned = vj.features.get_area_sum(integral_image, top_left,
                                    height, width)
        assert returned == 4.0



