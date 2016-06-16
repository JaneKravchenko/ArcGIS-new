import gdal
import numpy as np

def read_srtm(path):
    """
    :param path: way to .tif file
    :return: numpy array dtype: float32
    """
    print 'Download raster. Please, wait..'
    image = gdal.Open(path)
    print 'Download raster done!'
    return image.ReadAsArray().astype(np.float32)