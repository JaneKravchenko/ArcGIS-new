import flow_conditions

def calculate_step(matrix,old_matrix, posi, posj):
    step = []
    new_matrix = matrix*0
    def recur_current(matrix,posi, posj):
        if flow_conditions.current(matrix, posi, posj) == -1:
            return step
        else:
            res = flow_conditions.current(matrix, posi, posj)
            posi = res[0]
            posj = res[1]
            if old_matrix[posi][posj] == 0:
                if not (posi,posj,1) in step:
                    step.append((posi,posj,1))
                else:
                    return step
            else:
                if not (posi, posj, 0) in step:
                    step.append((posi,posj,0))
                else:
                    return step
            return recur_current(matrix, posi, posj)
    step = recur_current(matrix, posi, posj)
    iter1 = 0
    for i in step:
        if i[2] == 1:
            iter1 += 1
        else:
            iter1 += i[2]
        new_matrix[i[0]][i[1]] = iter1
    return new_matrix