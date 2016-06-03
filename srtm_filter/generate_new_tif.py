import read_srtm
import moving_window
import calculate_expected_value
import recalculate
import scipy.misc

def generate_new_array(path, width, height):

    old_array = read_srtm.read_srtm(path)
    new_array = old_array
    for posi in range(len(old_array) - width-1):
        for posj in range(len(old_array[posi]) - height-1):
            print posi, posj
            temporary_array = moving_window.mowing_window(old_array, width, height,posi,posj)
            temp_dict = recalculate.recalculate_array(
                temporary_array,posi, posj,
                calculate_expected_value.calculate_expected_value(temporary_array),
                calculate_expected_value.calculate_std(temporary_array))
            new_array[temp_dict.keys()[0][0]][temp_dict.keys()[0][1]] = temp_dict.values()[0]
    return new_array


scipy.misc.imsave('/home/jane/Desktop/ArcGIS-new/test_filtered_tif.tif', generate_new_array('/home/jane/Desktop/ArcGIS-new/filtered_tif_2.tif',5,5))