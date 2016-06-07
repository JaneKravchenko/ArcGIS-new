import read_srtm
import moving_window
import calculate_expected_value
import recalculate
import gdal
import scipy.misc

def generate_new_array(path, width, height):

    old_array = read_srtm.read_srtm(path)
    new_array = old_array
    for posi in range(len(old_array) - width-1):
        for posj in range(len(old_array[posi]) - height-1):
            temporary_array = moving_window.mowing_window(old_array, width, height,posi,posj)
            temp_dict = recalculate.recalculate_array(
                temporary_array,posi, posj,
                calculate_expected_value.calculate_std(temporary_array),
                calculate_expected_value.calculate_expected_value(temporary_array))
            if temp_dict.values()[0] <= 0.0:
                new_array[temp_dict.keys()[0][0]][temp_dict.keys()[0][1]] = 0.0
                print '( ' + str(posi) + ',' + str(posj) + ' )' + ': ' + str(96.0)
            else:
                new_array[temp_dict.keys()[0][0]][temp_dict.keys()[0][1]] = temp_dict.values()[0]
                print '( '+ str(posi) + ',' + str(posj)+ ' )'+': '+ str(temp_dict.values()[0])
    return new_array
array_n = generate_new_array('/home/jane/Desktop/ArcGIS-new/clipped_all_map.tif',3,3)


def saveRaster(outPath, etalonPath, array):
    gdalData = gdal.Open(etalonPath)
    projection = gdalData.GetProjection()
    transform = gdalData.GetGeoTransform()
    xsize = gdalData.RasterXSize
    ysize = gdalData.RasterYSize
    gdalData = None

    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    metadata = driver.GetMetadata()
    if metadata.has_key(gdal.DCAP_CREATE) and metadata[gdal.DCAP_CREATE] == "YES":
        outRaster = driver.Create(outPath, xsize, ysize, 1, gdal.GDT_Byte)
        outRaster.SetProjection(projection)
        outRaster.SetGeoTransform(transform)
        outRaster.GetRasterBand(1).WriteArray(array)
        outRaster = None
    else:
        print "Driver %s does not support Create() method." % format
        return False

saveRaster('/home/jane/Desktop/ArcGIS-new/clipped_all_map_f.tif', '/home/jane/Desktop/ArcGIS-new/clipped_all_map.tif', array_n)