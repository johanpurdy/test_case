import turtle

# Координаты многоугольников (списки кортежей)
polygons = [
    [(0, 0), (100, 0), (100, 100), (0, 100)],
    [(50, 50), (150, 50), (150, 150), (50, 150)],
    [(80, -20), (180, -20), (130, 80)]
]


def get_intersection(p1, p2, p3, p4):
    """Находит точку пересечения двух отрезков"""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    det = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if det == 0:
        return None

    inter_param_1 = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / det
    inter_param_2 = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / det

    if 0 <= inter_param_1 <= 1 and 0 <= inter_param_2 <= 1:
        x = x1 + inter_param_1 * (x2 - x1)
        y = y1 + inter_param_1 * (y2 - y1)
        return (x, y)
    return None


def is_inside(p, poly):
    """ Проверка: находится ли точка p внутри многоугольника"""
    x, y = p
    n = len(poly)
    inside = False
    for i in range(n):
        p1x, p1y = poly[i]
        p2x, p2y = poly[(i + 1) % n]
        if ((p1y > y) != (p2y > y)) and \
           (x < (p2x - p1x) * (y - p1y) / (p2y - p1y) + p1x):
            inside = not inside
    return inside
