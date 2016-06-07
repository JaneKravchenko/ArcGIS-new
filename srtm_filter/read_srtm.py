import gdal
import numpy as np

'''def read_srtm(path):
    """
    :param path: way to .tif file
    :return: numpy array dtype: float32
    """
    image = gdal.Open(path)
    return image.ReadAsArray().astype(np.float32)'''



read_srtm = lambda path: gdal.Open(path).ReadAsArray().astype(np.float32)
