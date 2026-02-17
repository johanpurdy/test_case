import turtle


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
        y = y1 + inter_param_2 * (y2 - y1)
        return (x, y)
    return None
