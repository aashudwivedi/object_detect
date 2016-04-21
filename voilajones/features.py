import numpy as np


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
