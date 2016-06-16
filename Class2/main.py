import read # Import file for read '*.tif'
import gdal
import os
import re

class Raster(object):

    def __init__(self, inpath):
        # Some facilities. Will be activate the next methods.
        self.name = None
        self.basename = None
        self.extention = None
        self.width  = None
        self.height = None
        self.path = inpath
        self.bands = None
        self.inarray = None

    def set_facilities(self):
        self.inarray = read.read_srtm(self.path)
        self.name = str(re.findall('\w.\w*', os.path.basename(self.path))[0])
        self.extention = '.'+ str(re.findall('\w.\w*', os.path.basename(self.path))[1])
        self.basename = self.name + self.extention
        self.width = gdal.Open(self.path).GetXSize

obj = Raster('/home/jane/Desktop/ArcGIS-new/SRTM/Flow/Flow/BT_flow.tif')
obj.set_facilities()
print obj.name
print obj.extention
print obj.basename