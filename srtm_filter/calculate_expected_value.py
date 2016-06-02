import numpy as np


def calculate_expected_value(input_temp_array):
    """
    :param input_temp_array: array of value of moving window
    :return: float value of mean
    """
    temp = []
    for i in input_temp_array:
        for j in i:
            temp.append(j)
    return np.mean(temp)

def calculate_std(input_temp_array):
    """
    :param input_temp_array: array of value of moving window
    :return: float value of std
    """
    temp = []
    for i in input_temp_array:
        for j in i:
            temp.append(j)
    return np.std(temp)