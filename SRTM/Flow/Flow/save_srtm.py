import gdal

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
