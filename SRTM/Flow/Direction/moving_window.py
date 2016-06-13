import numpy as np
def mowing_window(input_matrix, posi, posj):
    """
    :param input_matrix: must be array of srtm Z-value
    :param posi: index i of the upper left corner window position
    :param posj: index j of the upper left corner window position
    :return: temporary array of values which moving window included
    """


    # create range of path/row walue
    range_i = range(posi, posi + 3)
    range_j = range(posj, posj + 3)
    # generate a temporary array
    return np.array(map(lambda i: map(lambda j: input_matrix[i][j], range_j), range_i))