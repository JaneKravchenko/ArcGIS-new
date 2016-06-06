import re
def get_value(path, line_name):
    infile = open(path)
    lines = infile.readlines()
    for line in lines:
        if line_name in line:
            index = line.index(line_name[-1])
            num = re.findall(r'\w+', line[index+1:])
            if len(num) == 2:
                return float(str(num[0])+'.'+str(num[1]))
            else:
                return int(num[0])


"""Enter path to metadata file:
/home/jane/Desktop/ArcGIS-new/LE71820252002235SGS00/LE71820252002235SGS00_MTL.txt
Enter a list of need parameters:
RADIANCE_MAXIMUM_BAND_6_VCID_2,
RADIANCE_MINIMUM_BAND_6_VCID_2,
QUANTIZE_CAL_MAX_BAND_6_VCID_2,
QUANTIZE_CAL_MIN_BAND_6_VCID_2"""


def get_all_parameter():
    path = str(raw_input('Enter path to metadata file: '))
    values = str(raw_input('Enter a list of need parameters: '))
    val = values.split(',')
    temp = []
    for i in val:
        temp.append(get_value(path, i))
    return temp 
print get_all_parameter()
