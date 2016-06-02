import gdal
import numpy as np

def read_srtm(path):
    """
    :param path: way to .tif file
    :return: numpy array dtype: float32
    """
    image = gdal.Open(path)
    imarray = image.GetRasterBand(1)
    return imarray.ReadAsArray().astype(np.float32)
