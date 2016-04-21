import numpy as np


def get_integral_image(image):
    result = np.zeros(image.shape)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            result[i][j] = image[i][j]
            summand_indexes = [(i - 1, j), (i, j - 1)]
            for index in summand_indexes:
                try:
                    result[i][j] += image[index[0]][index[1]]
                except IndexError:
                    pass
    return result
