import gdal
import os
import re
import numpy as np

import dir_recalculate
import calculate_expected_value
import filter_recalculate
import moving_window
import read
import save
import define_direction_null
import flow_calculate_step
import radiance
import temperature
import g_albedo


class Raster(object):
    def __init__(self, inpath):

        """
        :param inpath: path to raster file
        """

        # Some facilities. Will be activate the next methods.

        # Overall
        self.name = None
        self.basename = None
        self.extention = None
        self.width = None
        self.height = None
        self.path = inpath
        self.inarray = None
        self.projection = None
        self.transformation = None

        # SRTM
        self.filter_array = None
        self.dir_array = None
        self.flow_array = None

        # Landsat
        self.radmin = None
        self.radmax = None
        self.qmin = None
        self.qmax = None
        self.k1 = None
        self.k2 = None
        self.rad = None
        self.temperature = None
        self.earth_sun_distance = None
        self.albedo_array = None
        self.sun_elevation = None


# set facilities ------------------------------------------------------------------------------------------------------

    def set_facilities(self):
        """
        :return: all possible facilities
        """
        print 'Set facilities. Please, wait..'
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
        print 'Done!'

# filter ---------------------------------------------------------------------------------------------------------------

    def filter(self, outpath, width, height):

        """
        :param outpath: path to save out raster, have to be with extention .tif
        :param width: mv window size
        :param height: mv size
        :return: filtered array, possible to get like .filter_array properties; save raster to define out path
        """
        print 'Filtering. Please, wait..'
        # initialize initial filter array
        self.filter_array = self.inarray

        # loop for move window
        for posi in range(len(self.inarray) - width - 1):
            for posj in range(len(self.inarray[posi]) - height - 1):

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
        print 'Filtering done!'

# direction ------------------------------------------------------------------------------------------------------------

    def get_direction(self, outpath, fltr_array):

        """
        :param fltr_array: can be numpy array os path to file
        :param outpath: path to save out tif
        :return: nothing, only save file and set the value self.dir_array
        """
        # print status
        print 'Calculate direction. Please, wait..'

        # The condition for case, when filter array is path to file, instead of numpy array
        if type(fltr_array) == str:
            temp = read.read_srtm(fltr_array)
            fltr_array = temp

        # generate new empty array
        self.dir_array = np.array(
            map(lambda row: map(lambda path: -1, range(len(fltr_array[row]))), range(len(fltr_array))))

        # calculate direction
        for i in range(len(fltr_array) - 3):
            for j in range(len(fltr_array[i]) - 3):
                temp_dict = dir_recalculate.recalculate_array(moving_window.mowing_window(fltr_array, 3, 3, i, j), i, j)
                self.dir_array[temp_dict.keys()[0][0]][temp_dict.keys()[0][1]] = temp_dict.values()[0]

        # save raster to out path
        save.saveRaster(outpath, self.path, self.dir_array)

        # print status
        print 'Calculate direction done!'

# flow ----------------------------------------------------------------------------------------------------------------

    def flow(self, outpath, dir_array):

        """
        :param outpath: path to save file
        :param dir_array: array with directory value
        :return: nothing, only save file and set value self.
        """

        # print status
        print 'Calculate flow. Please, wait..'

        # The condition for case, when filter array is path to file, instead of numpy array
        if type(dir_array) == str:
            temp = read.read_srtm(dir_array)
            dir_array = temp

        # calculate array for null destination
        null = define_direction_null.define_pos_null(dir_array)

        # generate first matrix value
        list_of_matrix_value = flow_calculate_step.calculate_step(dir_array, dir_array * 0, null[0][0], null[0][0])
        old_matrix = flow_calculate_step.calculate_step(dir_array, dir_array * 0, null[0][0], null[0][0])

        # calculate flow accomulation
        for i in null:
            old_matrix = flow_calculate_step.calculate_step(dir_array, old_matrix, i[0], i[1])
            list_of_matrix_value += flow_calculate_step.calculate_step(dir_array, old_matrix, i[0], i[1])

        self.flow_array = list_of_matrix_value

        # calculate median value without null value
        med = []
        for i in self.flow_array:
            for j in i:
                if j != 0:
                    med.append(j)
        median = np.median(med)

        # this condition for generate a binary tif
        for i in range(len(self.flow_array)):
            for j in range(len(self.flow_array[i])):
                if self.flow_array[i, j] <= median:
                    self.flow_array[i, j] = 0
                else:
                    self.flow_array[i, j] = 1

        # save raster to out path
        save.saveRaster(outpath, self.path, self.flow_array)

        # print status
        print ' Calculate flow done!'

# metadata read ------------------------------------------------------------------------------------------------------

    def read_metadata(self, metadata_path, param):

        """
        :param metadata_path: path to metadata file
        :param param: name of line
        :return: float number
        """
        # print status
        print 'Read metadata..'

        # open metadata file
        infile = open(metadata_path).readlines()

        # read file line by line and find a needed line
        for line in infile:
            num = re.findall(param + '\s*=\s*([0-9.]+)', line)
            if len(num) >= 1:
                return float(num[0])

        # print status
        print 'Read metadata done!'

# metadata set -------------------------------------------------------------------------------------------------------

    def set_parameters_from_metadata(self, metadata_path, LC_num):

        """
        :param metadata_path: path to metadata file
        :param LC_num: landsat number
        :return: nothing
        """
        # print status
        print 'Set metadata parameters..'

        # set parameters for 7 landsat
        if LC_num == 7:

            # radiance maximum
            self.radmax = self.read_metadata(metadata_path, 'RADIANCE_MAXIMUM_BAND_6_VCID_2')

            # radiance minimum
            self.radmin = self.read_metadata(metadata_path, 'RADIANCE_MINIMUM_BAND_6_VCID_2')

            # quantize maximum
            self.qmax = self.read_metadata(metadata_path, 'QUANTIZE_CAL_MAX_BAND_6_VCID_2')

            # quantize minimum
            self.qmin = self.read_metadata(metadata_path, 'QUANTIZE_CAL_MIN_BAND_6_VCID_2')

            # constant K1
            self.k1 = self.read_metadata(metadata_path, 'K1_CONSTANT_BAND_6_VCID_2')

            # constant K2
            self.k2 = self.read_metadata(metadata_path, 'K2_CONSTANT_BAND_6_VCID_2')

            # distance to sun
            self.earth_sun_distance = self.read_metadata(metadata_path, 'EARTH_SUN_DISTANCE')

            # sun elevation (radian --> degree)
            self.sun_elevation = float(self.read_metadata(metadata_path, 'SUN_ELEVATION')) * 57.2958

            # print status
            print 'Set metadata parameters done!'

# radiance -----------------------------------------------------------------------------------------------------------

    def get_radiance(self):

        """
        :return: radiance array
        """
        # print status
        print 'Calculate radiance..'

        # set self.rad
        self.rad = radiance.radiance(self.inarray, self.qmin, self.qmax, self.radmin, self.radmax)

        # print status
        print 'Calculate radiance done!'

        return self.rad

# temperature --------------------------------------------------------------------------------------------------------

    def get_temperature(self, outpath):

        """
        :param outpath: path to out file with temperature values
        :return: set self.temperature, nothing
        """
        # print status
        print 'Calculate temperature..'

        # set self.temperature
        self.temperature = temperature.temperature(self.k2, self.k1, self.rad)

        # save raster to out path
        save.saveRaster(outpath, self.path, self.temperature)

        # print status
        print 'Calculate temperature done!'

# albedo -------------------------------------------------------------------------------------------------------------

    def get_albedo(self, outpath):

        """
        :param outpath: path to albedo raster
        :return:
        """

        # print status
        print 'Calculate albedo..'

        self.albedo_array = g_albedo.albedo(self.rad, self.earth_sun_distance, self.sun_elevation, 7, 3)*100
        save.saveRaster(outpath, self.path, self.albedo_array)

        # print status
        print 'Calculate albedo done!'

'''obj = Raster('/home/jane/Desktop/ArcGIS-new/Test_Class/test5.tif')
obj.set_facilities()
obj.get_direction('/home/jane/Desktop/ArcGIS-new/Test_Class/dir.tif', '/home/jane/Desktop/ArcGIS-new/Test_Class/test5.tif')
obj.flow('/home/jane/Desktop/ArcGIS-new/Test_Class/flow.tif', '/home/jane/Desktop/ArcGIS-new/Test_Class/dir.tif' )
print 'All Done!


obj = Raster('/home/jane/Desktop/ArcGIS-new/LE71820252002235SGS00/LE71820252002235SGS00_B3.TIF')
obj.set_facilities()
obj.set_parameters_from_metadata('/home/jane/Desktop/ArcGIS-new/LE71820252002235SGS00/LE71820252002235SGS00_MTL.txt',7)
obj.get_radiance()
save.saveRaster('/home/jane/Desktop/ArcGIS-new/rad.tif', obj.path, obj.rad)
print obj.earth_sun_distance, obj.sun_elevation
obj.get_albedo('/home/jane/Desktop/ArcGIS-new/albedo.tif')'''
