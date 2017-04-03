from math import sqrt


def distance(a, b):
    return sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))


def validate_item(room_map, new_item):
    return room_map[new_item[0]][new_item[1]] == '_'

def validate_wall_item(room_map, new_item):
    item_x, item_y = new_item
    dim_x = len(room_map[0])
    dim_y = len(room_map)
    ok_flag = True

    if item_x == 0 or item_y == 0 or item_x == dim_x-1 or item_y == dim_y-1:
        return False

    if room_map[item_x][item_y] != '_':
        ok_flag = False

    if room_map[item_x+1][item_y] != '_':
        ok_flag = False

    if room_map[item_x-1][item_y] != '_':
        ok_flag = False

    if room_map[item_x][item_y+1] != '_':
        ok_flag = False

    if room_map[item_x][item_y-1] != '_':
        ok_flag = False

    if room_map[item_x+1][item_y+1] != '_':
        ok_flag = False

    if room_map[item_x-1][item_y-1] != '_':
        ok_flag = False

    if room_map[item_x+1][item_y-1] != '_':
        ok_flag = False

    if room_map[item_x-1][item_y+1] != '_':
        ok_flag = False

    return ok_flag

