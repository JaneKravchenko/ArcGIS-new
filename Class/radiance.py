def radiance(array, q_min, q_max, rad_min, rad_max):

    """
    :param array: your raster written as array
    :param q_min: Q_min and Q_max - MIN_MAX_PIXEL_VALUE from metadata
    :param q_max: Q_min and Q_max - MIN_MAX_PIXEL_VALUE from metadata
    :param rad_min: MIN_MAX_RADIANCE from metadata
    :param rad_max: MIN_MAX_RADIANCE from metadata
    :return: radiance which gonna be calculated by this function
    """

    return ((rad_max - rad_min)/(
        q_max - q_min)) * (array - q_min) + rad_min