import utils.samath as sm


TILE_SIZE = 20

def cvt_str_to_tile(string):

    x, y = string.split(";")
    x = int(x) * TILE_SIZE
    y = int(y) * TILE_SIZE

    return (x, y)

def cvt_tile_to_str(position):
    x, y = position
    x = int(x // TILE_SIZE)
    y = int(y // TILE_SIZE)

    return str(x) + ";" + str(y)


def check_pt_on_line(start: list, end: list, point: list, error=0):
    dist_ab = sm.distance(start, end)
    dist_ac = sm.distance(start, point)
    dist_bc = sm.distance(end, point)
    return abs(dist_ab - (dist_ac + dist_bc)) < error