import gdal
import numpy as np
read_srtm = lambda path: gdal.Open(path).ReadAsArray().astype(np.float32)