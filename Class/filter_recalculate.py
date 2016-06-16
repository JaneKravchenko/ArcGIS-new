import numpy as np
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
        mean_posi = width/2
        mean_posj = width/2
        if temp_array[mean_posi][mean_posj] > mean-std and temp_array[mean_posi][mean_posj] < mean+std:
            return {(mean_posi+posi, mean_posj+posj): temp_array[mean_posi][mean_posj]}
        else:
            normal_value = []
            for i in temp_array:
                for j in i:
                    if j <= mean+(2*std) and j >= mean-(2*std):
                        normal_value.append(j)
            if len(normal_value) > 1:
                mean = np.mean(normal_value)
                print '+++ '+ str(mean)
                return {(mean_posi+posi, mean_posj+posj): mean}
            else:
                print 'Not changed mean: '+ str(mean)
                return {(mean_posi + posi, mean_posj + posj): mean}
    else:
        return str('Moving window width and height mus be unpaired')