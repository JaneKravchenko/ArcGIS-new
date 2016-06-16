import math


def albedo(radiance, sun_distance, sun_elevation, LC_number, band_number):
    """
    :param radiance: radiance
    :param sun_distance: earth sun distance
    :param E: lumosity factor of each channel
    :param sun_elevation: sun elevation
    :param LC_number: landsat number
    :param band_number: number of bend
    :return: array which will consist information about surface albedo
    """

    # lumosity factor of each channel
    LC7 = [0, 1969.000, 1840.000, 1551.000, 1044.000, 225.700, 82.07, 1368.000]
    LC8 = [0, 1969.000, 1840.000, 225.700, 1551.000, 1044.000, 82.07, 1368.000]

    if LC_number == 7:
        E = float(LC7[band_number])

    if LC_number == 8:
        E = float(LC8[band_number])

    return (math.pi * radiance * (sun_distance ** 2)) / (E * math.sin(sun_elevation))
