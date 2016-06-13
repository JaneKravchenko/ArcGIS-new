import moving_window
def current(matrix, posi, posj):
    val = int(matrix[posi][posj])
    if val == 0:
        if posi!=0 and posj!=0 and matrix[posi-1][posj-1]!=8:
            return posi-1, posj-1
        else:
            return -1
    if val == 1:
        if posi != 0 and matrix[posi-1][posj] != 7:
            return posi-1,posj
        else:
            return -1
    if val == 2:
        if posi!=0 and posj < len(matrix)-1 and matrix[posi-1][posj+1] != 6:
            return posi -1, posj+1
        else:
            return -1
    if val == 3:
        if posj != 0 and matrix[posi][posj-1] != 5:
            return posi, posj-1
        else:
            return -1
    if val == 5:
        if posj < len(matrix)-1 and matrix[posi][ posj+1] != 3:
            return posi, posj+1
        else:
            return -1
    if val == 6:
        if posj!=0 and posi<len(matrix)-1 and matrix[posi+1][posj-1] != 2:
            return posi+1,posj-1
        return -1
    if val == 7:
        if posi<len(matrix)-1 and matrix[posi+1][posj] != 1:
            return posi+1, posj
        else:
            return -1
    if val == 8:
        if posi<len(matrix)-1 and posj<len(matrix)-1 and matrix[posi+1][posj+1] != 0:
            return posi+1, posj+1
        else:
            return -1