def recalculate_array(temp_array,posi, posj):
    """
    :param temp_array: temporary moving window array
    :param posi: current moving window position i
    :param posj: current moving window position j
    :param std: std of moving window array
    :param mean: mean of moving window array
    :return: dictionary, when key - is position and value - is value
    """
    temp_array.shape = 9
    temp = []
    for i in temp_array:
        if (temp_array[4] - i) > 0:
            temp.append(temp_array[4] - i)
        else:
            temp.append(0)
    for i in range(len(temp)):
        if i%2 == 0:
            temp[i] = float(temp[i])/(2**(0.5))
    return {(posi+1, posj+1): temp.index(max(temp))}
