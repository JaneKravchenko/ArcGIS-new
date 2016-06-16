import moving_window

def define_pos_null(ray):
    list_of_point_null = []
    for posi in range(len(ray) - 2):
        for posj in range(len(ray[posi]) - 2):
            temp_ray = moving_window.mowing_window(ray, 3, 3, posi, posj)
            temp_ray.shape = 9
            k = 0
            for i in range(len(temp_ray)):
                if i + temp_ray[i] == 8:
                    k += 1
            if k == 0:
                list_of_point_null.append((posi + 1, posj + 1))

    for posi in range(len(ray) - 1):
        temp_ray = moving_window.mowing_window(ray, 2, 2, posi, 0)
        temp_ray.shape = 4
        k = 0
        for i in range(len(temp_ray)):
            if i + temp_ray[i] + 5 == 8:
                k += 1
        if k == 0:
            if not (posi, 0) in list_of_point_null:
                list_of_point_null.append((posi, 0))

    for posj in range(len(ray) - 1):
        temp_ray = moving_window.mowing_window(ray, 2, 2, 0, posj)
        temp_ray.shape = 4
        k = 0
        for i in range(len(temp_ray)):
            if i + temp_ray[i] + 5 == 8:
                k += 1
        if k == 0:
            if not (0, posj) in list_of_point_null:
                list_of_point_null.append((0, posj))

    return list_of_point_null