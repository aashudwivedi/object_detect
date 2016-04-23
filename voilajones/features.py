import numpy as np
from collections import namedtuple


class Feature(object):
    def __init__(self, integral_image, position, width, height):
        """
        :param integral_image: summed area table of the image
        :param top_left: coordinates of the top left point
        :param bottom_right: coordinates of the bottom right point
        """
        self.integral_image = integral_image

    def get_score(self):
        raise NotImplementedError('Not implemented use a subclass')

    @property
    def type(self):
        raise NotImplemented('Not implemented use a subclass')


class FEATURE_TYPES:
    TWO_VERTICAL = TwoRectangleVertical


class TwoRectangleVertical(Feature):
    type = FEATURE_TYPES.TWO_VERTICAL

    def get_score(self):
        rect_height = self.height / 2
        rec_width = self.width

        top_left = self.position
        top = get_area_sum(self.integral_image, top_left,
                           rect_height, rec_width)

        top_left = (self.position[0] + rect_height, self.position[1])
        bottom = get_area_sum(self.integral_image, top_left,
                                rect_height, rec_width)

        return bottom - top


def get_integral_image(image):
    """
    calculates the summed area table for the image
    in a single pass
    :param image: image
    :return: summed area table (integral image)
    """
    result = np.zeros(image.shape)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            result[i][j] = image[i][j]
            if i - 1 >= 0:
                result[i][j] += result[i-1][j]
            if j - 1 >= 0:
                result[i][j] += result[i][j-1]
            if i - 1 >= 0 and j - 1 >= 0:
                result[i][j] -= result[i-1][j-1]
    return result


def get_area_sum(integral_image, top_left, height, width):
    top_right = (top_left[0], top_left[1] + width)
    bottom_right = (top_right[0] + height, top_right[1])
    bottom_left = (top_left[0] + height, top_left[1])

    return (integral_image[top_left] + integral_image[bottom_right] -
            integral_image[top_right] - integral_image[bottom_left])



def get_feature(feature_type, x, y, width, height):
    """

    :param feature_type:
    :param x:
    :param y:
    :param width:
    :param height:
    :return:
    """
