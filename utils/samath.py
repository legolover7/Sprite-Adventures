

def distance(point1: list, point2: list) -> float:
    """Takes in two points and returns the distance between them"""
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
