

def collides_point(point=(0, 0), rect=(0, 0, 0, 0), circle=(0, 0, 0)):
    """Rect: (x, y, width, height) | Circle: (x, y, radius)"""
    if rect != (0, 0, 0, 0):
        return rect[0] < point[0] < rect[0] + rect[2] and rect[1] < point[1] < rect[1] + rect[3]

    elif circle != (0, 0):
        if ((point[0] - circle[0])**2 + (point[1] - circle[1])**2) ** 0.5 <= circle[2]:
            return True
        

def collides_point_circle(point, position, radius):
    diff_x, diff_y = point[0] - position[0], point[1] - position[1]
    distance = (diff_x ** 2 + diff_y ** 2) ** 0.5
    return distance <= radius