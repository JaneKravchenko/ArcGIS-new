import load_srtm
import save_srtm
import define_null
import calculate_step


def run(inpath, outpath):
    matrix = load_srtm.read_srtm(inpath)
    print 'Matrix had been loaded'
    null = define_null.define_pos_null(matrix)
    list_of_matrix_value = calculate_step.calculate_step(matrix, matrix*0, null[0][0], null[0][0])
    'In list of matrix value added first element'
    old_matrix = calculate_step.calculate_step(matrix, matrix*0, null[0][0], null[0][0])
    for i in null:
        print i
        old_matrix = calculate_step.calculate_step(matrix, old_matrix, i[0], i[1])
        list_of_matrix_value+=calculate_step.calculate_step(matrix, old_matrix, i[0], i[1])
    array = list_of_matrix_value
    save_srtm.saveRaster(outpath, inpath, array)

run('/home/jane/Desktop/single_flow_direction/clipped_dir.tif', '/home/jane/Desktop/ArcGIS-new/SRTM/V _flow.tif')