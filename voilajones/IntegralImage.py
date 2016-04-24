import cv2
import numpy as np


def get_area_sum(integral_image, top_left, height, width):
    """
    calculates the area sum for the integral image

    :param integral_image:
    :param top_left:
    :param height:
    :param width:
    :return:
    """
    top_right = (top_left[0], top_left[1] + width)
    bottom_right = (top_right[0] + height, top_right[1])
    bottom_left = (top_left[0] + height, top_left[1])

    return (integral_image[top_left] + integral_image[bottom_right] -
            integral_image[top_right] - integral_image[bottom_left])


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
    result = np.hstack((np.zeros((result.shape[0], 1)), result))
    result = np.vstack((np.zeros((1, result.shape[1])), result))
    return result


class IntegralImage:

    def __init__(self, orig_image, label):
        self.sum = 0
        self.label = label
        self.calculate_integral(orig_image)
        self.weight = 0
    
    def calculate_integral(self, orig_image):
        self.integral = get_integral_image(orig_image)
    
    def get_area_sum(self, topLeft, bottomRight):
        '''
        Calculates the sum in the rectangle specified by the given tuples.
        @param topLeft: (x,y) of the rectangle's top left corner
        @param bottomRight: (x,y) of the rectangle's bottom right corner
        '''

        # swap tuples
        topLeft = (topLeft[1], topLeft[0])
        bottomRight = (bottomRight[1], bottomRight[0])

        height = bottomRight[0] - topLeft[0]
        width = bottomRight[1] - topLeft[1]

        return get_area_sum(self.integral, topLeft, height, width)

    def set_label(self, label):
        self.label = label
    
    def set_weight(self, weight):
        self.weight = weight