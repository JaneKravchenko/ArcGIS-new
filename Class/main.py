import gdal
import os
import re
import numpy as np

import dir_recalculate
import calculate_expected_value
import filter_recalculate
import moving_window
import read  # Import file for read '*.tif'
import save


class Raster(object):
    def __init__(self, inpath):

        """
        :param inpath: path to raster file
        """

        # Some facilities. Will be activate the next methods.

        self.name = None
        self.basename = None
        self.extention = None
        self.width = None
        self.height = None
        self.path = inpath
        self.bands = None
        self.inarray = None
        self.projection = None
        self.transformation = None
        self.filter_array = None
        self.dir_array = None

    def set_facilities(self):
        """
        :return: all possible facilities
        """

        # raster like numpy array
        self.inarray = read.read_srtm(self.path)

        # name without extention and path
        self.name = str(re.findall('\w.\w*', os.path.basename(self.path))[0])

        # extention with dot
        self.extention = '.' + str(re.findall('\w.\w*', os.path.basename(self.path))[1])

        # full name without path
        self.basename = self.name + self.extention

        # open raster for get some parameters
        object = gdal.Open(self.path)

        # width, height: raster size
        self.width = str(object.RasterXSize) + ' pixels.'
        self.height = str(object.RasterYSize) + ' pixels.'

        # raster projection
        self.projection = str(object.GetProjection())

        # raster transformation
        self.transformation = str(object.GetGeoTransform())

    def filter(self, outpath, width, height):

        """
        :param outpath: path to save out raster, have to be with extention .tif
        :param width: mv window size
        :param height: mv size
        :return: filtered array, possible to get like .filter_array properties; save raster to define out path
        """

        # initialize initial filter array
        self.filter_array = self.inarray

        # loop for move window
        for posi in range(len(self.inarray) - width - 1):
            for posj in range(len(self.inarray[posi]) - height - 1):

                # create temporary array, which get values in temp window
                temporary_array = moving_window.mowing_window(self.inarray, width, height, posi, posj)

                # dictionary, where key - is position and value - is value
                temp_dict = filter_recalculate.recalculate_array(
                    temporary_array, posi, posj,
                    calculate_expected_value.calculate_std(temporary_array),
                    calculate_expected_value.calculate_expected_value(temporary_array))

                # it doesn't matter, program need this conditions
                if temp_dict.values()[0] <= 0.0:
                    self.filter_array[temp_dict.keys()[0][0]][temp_dict.keys()[0][1]] = 0.0
                else:
                    self.filter_array[temp_dict.keys()[0][0]][temp_dict.keys()[0][1]] = temp_dict.values()[0]

        # save raster to out path
        save.saveRaster(outpath, self.path, self.filter_array)

    def get_direction(self, outpath):
        self.dir_array = np.array(
            map(lambda row: map(lambda path: -1, range(len(self.inarray[row]))), range(len(self.inarray))))
        for i in range(len(self.inarray) - 3):
            for j in range(len(self.inarray[i]) - 3):
                temp_dict = dir_recalculate.recalculate_array(moving_window.mowing_window(self.inarray, i, j), i, j)
                self.dir_array[temp_dict.keys()[0][0]][temp_dict.keys()[0][1]] = temp_dict.values()[0]
        save.saveRaster(outpath, self.path, self.dir_array)


obj = Raster('/home/jane/Desktop/ArcGIS-new/SRTM/Flow/Flow/BT_flow.tif')
obj.set_facilities()
print 'name: ' + obj.name + '\n'
print 'extention: ' + obj.extention + '\n'
print 'basename: ' + obj.basename + '\n'
print 'width: ' + obj.width + '\n'
print 'height: ' + obj.height + '\n'
print 'projection: ' + obj.projection + '\n'
print 'transformation: ' + obj.transformation + '\n'
print 'path: ' + obj.path
