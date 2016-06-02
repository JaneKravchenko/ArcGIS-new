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
    range_i = range(posi, posi+width)
    range_j = range(posj, posj+height)
    # generate a temporary array
    return map(lambda i, j: input_matrix[i][j], range_i, range_j)
