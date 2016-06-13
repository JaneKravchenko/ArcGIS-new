import numpy as np
import gdal

matrix = read_srtm('/home/jane/Desktop/ArcGIS-new/SRTM/Vuzgorod_direction.tif')

null = define_pos_null(matrix)
mat = []
mat.append(calculate_step(matrix, matrix*0, null[0][0], null[0][1]))
for i in null[1:]:
    print i
    mat.append(calculate_step(matrix,mat[-1], i[0], i[1]))
array  = sum(mat)
saveRaster('/home/jane/Desktop/ArcGIS-new/SRTM/Vuzgorod_flow.tif', '/home/jane/Desktop/ArcGIS-new/SRTM/Vuzgorod_direction.tif', array)

