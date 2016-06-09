import numpy as np
import gdal
read_srtm = lambda path: gdal.Open(path).ReadAsArray().astype(np.float32)
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
matrix = read_srtm('/home/jane/Desktop/single_flow_direction/ed_direct.tif')
print matrix
def mowing_window(
        input_matrix,w,h, posi, posj):
    # create range of path/row walue
    range_i = range(posi, posi+w)
    range_j = range(posj, posj+h)
    # generate a temporary array
    return np.array(map(lambda i: map(lambda j: input_matrix[i][j], range_j),range_i))

def current(matrix, posi, posj):
    val = matrix[posi][posj]
    if val == 0:
        if posi!=0 and posj!=0:
            return (posi-1,posj-1)
        else:
            return -1
    if val == 1:
        if posi != 0:
            return (posi-1,posj)
        else:
            return -1
    if val == 2:
        if posi!=0 and posj<len(matrix)-1:
            return (posi -1, posj+1)
        else:
            return -1
    if val == 3:
        if posj!=0:
            return (posi, posj-1)
        else:
            return -1
    if val == 5:
        if posj<len(matrix)-1:
            return (posi, posj+1)
        else:
            return -1
    if val == 6:
        if posj!=0 and posi<len(matrix)-1:
            return (posi+1,posj-1)
        else:
            return -1
    if val == 7:
        if posi<len(matrix)-1:
            return (posi+1, posj)
        else:
            return -1
    if val == 8:
        if posi<len(matrix)-1 and posj<len(matrix)-1:
            return (posi+1, posj+1)
        else:
            return -1

def calculate_step(matrix,old_matrix, posi, posj):
    step = []
    new_matrix = matrix*0
    def recur_current(matrix,posi, posj):
        boundaryi = len(matrix) - 1
        boundaryj = len(matrix[0]) - 1
        if posi >= boundaryi:
            if posj >= boundaryj:
                pass
        else:
            res = current(matrix, posi, posj)
            if res!=-1:
                posi = res[0]
                posj = res[1]
                if old_matrix[posi][posj] == 0:
                    step.append((posi,posj,1))
                else:
                    step.append((posi,posj, 0))
                    
                return recur_current(matrix, posi, posj)
            else:
                return False
    recur_current(matrix, posi, posj)
    iter1 = 0
    for i in step:
        if i[2] ==1:
            iter1 +=1
        else:
            iter1 += i[2]
        new_matrix[i[0]][i[1]] = iter1
    return new_matrix

def define_pos_null(ray):
    list_of_point_null = []
    for posi in range(len(ray)-2):
        for posj in range(len(ray[posi])-2):
            temp_ray = mowing_window(ray,3,3, posi, posj)
            temp_ray.shape = 9
            k = 0
            for i in range(len(temp_ray)):
                if i + temp_ray[i] == 8:
                    k+=1
            if k == 0:
                list_of_point_null.append((posi+1, posj+1))
                
    for posi in range(len(ray)-1):
        temp_ray = mowing_window(ray,2,2, posi, 0)
        temp_ray.shape = 4
        k = 0
        for i in range(len(temp_ray)):
            if i + temp_ray[i] + 5 == 8:
                k+=1
        if k == 0:
            if not (posi, 0) in  list_of_point_null:
                list_of_point_null.append((posi, 0))
            
    for posj in range(len(ray)-1):
        temp_ray = mowing_window(ray,2,2, 0, posj)
        temp_ray.shape = 4
        k = 0
        for i in range(len(temp_ray)):
            if i + temp_ray[i] + 5 == 8:
                k+=1
        if k == 0:
            if not (0, posj) in list_of_point_null:
                list_of_point_null.append((0, posj))
    return list_of_point_null
null = define_pos_null(matrix)
mat = []
mat.append(calculate_step(matrix, matrix*0, null[0][0], null[0][1]))
for i in null[1:]:
    mat.append(calculate_step(matrix,mat[-1], i[0], i[1]))
array  = sum(mat)
saveRaster('/home/jane/Desktop/single_flow_direction/flow_1.tif', '/home/jane/Desktop/single_flow_direction/ed_direct.tif', array)
