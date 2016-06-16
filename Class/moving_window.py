import numpy as np

def mowing_window(
        input_matrix, width, height, posi, posj):
    """
    :param input_matrix: must be array of srtm Z-value
    :param width: moving window width, must be integer
    :param height: moving window height, must be integer
    :param posi: index i of the upper left corner window position
    :param posj: index j of the upper left corner window position
    :return: temporary array of values which moving window included
    """


    # create range of path/row walue
    range_i = range(posi, posi + width)
    range_j = range(posj, posj + height)
    # generate a temporary array
    for i in range_i:
        for j in range_j:
            if input_matrix[i][j] == -32768.0:
                input_matrix[i][j] = 0
    return np.array(map(lambda i: map(lambda j: input_matrix[i][j], range_j), range_i))