import load_srtm
import moving_window
import recalculate
import save_tif
import numpy as np

def run(inpath, outpath):
    raster = load_srtm.read_srtm(inpath)
    new_array = np.array(map(lambda i : map(lambda j: -1, range(len(raster[i]))), range(len(raster))))
    for i in range(len(raster)-3):
        for j in range(len(raster[i])-3):
            temp_dict = recalculate.recalculate_array(moving_window.mowing_window(raster, i, j), i, j)
            new_array[temp_dict.keys()[0][0]][temp_dict.keys()[0][1]] = temp_dict.values()[0]
            print str(i) + ',' + str(j) + ': ' + str(temp_dict.values()[0])
    save_tif.saveRaster(outpath, inpath, new_array)

run('/home/jane/Desktop/ArcGIS-new/SRTM/Flow/filter.tif', '/home/jane/Desktop/ArcGIS-new/SRTM/Flow/direction.tif')
