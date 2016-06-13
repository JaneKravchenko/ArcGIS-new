import numpy as np
def mowing_window(
        input_matrix, w, h, posi, posj):


    # create range of path/row walue
    range_i = range(posi, posi + w)
    range_j = range(posj, posj + h)
    # generate a temporary array
    return np.array(map(lambda i: map(lambda j: input_matrix[i][j], range_j), range_i))