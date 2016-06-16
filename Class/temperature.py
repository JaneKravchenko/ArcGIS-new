import numpy as np


def temperature(K2, K1, R):
    """
    :param K2: K2_CONSTANT_BAND_6 from metadata in GROUP = THERMAL_CONSTANTS
    :param K1: K1_CONSTANT_BAND_6 from metadata in GROUP = THERMAL_CONSTANTS
    :param R: radiance
    :return: array which will consist information about temperature map
    """

    return (K2/(np.log(K1/R+1))) - 273
