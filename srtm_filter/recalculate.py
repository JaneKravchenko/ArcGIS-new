def recalculate_array(temp_array,posi, posj, std, mean):
    """
    :param temp_array: temporary moving window array
    :param posi: current moving window position i
    :param posj: current moving window position j
    :param std: std of moving window array
    :param mean: mean of moving window array
    :return: dictionary, when key - is position and value - is value
    """
    width = len(temp_array)
    if width%2 == 1:
        mean_posi = width/2+1
        mean_posj = width/2+1
        if temp_array[mean_posi][mean_posj] in range(mean-std, mean+std):
            return {(mean_posi+posi, mean_posj+posj): temp_array[mean_posi][mean_posj]}
        else:
            return {(mean_posi+posi, mean_posj+posj): temp_array[mean_posi][mean_posj]}
    else:
        return str('Moving window width and height mus be unpaired')