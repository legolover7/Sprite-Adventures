
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