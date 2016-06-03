import read_srtm
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
    new_array = []
    for i in range_i:
        new_array.append(map(lambda j: input_matrix[i][j], range_j))
    return new_array

#print mowing_window(read_srtm.read_srtm('/home/jane/Desktop/ArcGIS-new/clipped_all_map.tif'),5,5,0,0)
