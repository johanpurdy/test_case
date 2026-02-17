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


def draw():
    t = turtle.Turtle()
    t.speed(0)

    # 1. Сначала рисуем исходные фигуры тонкими линиями
    t.pencolor("lightgray")
    for poly in polygons:
        t.up()
        t.goto(poly[0])
        t.down()
        for p in poly[1:] + [poly[0]]:
            t.goto(p)

    # 2. Ищем внешние сегменты
    t.pencolor("red")
    t.pensize(3)
    for i, poly in enumerate(polygons):
        for j in range(len(poly)):
            p1, p2 = poly[j], poly[(j + 1) % len(poly)]
            # Разбиваем сторону на мелкие отрезки для проверки
            steps = 50 
            for s in range(steps):
                curr = (p1[0] + (p2[0]-p1[0])*s/steps, p1[1] + (p2[1]-p1[1])*s/steps)
                next_p = (p1[0] + (p2[0]-p1[0])*(s+1)/steps, p1[1] + (p2[1]-p1[1])*(s+1)/steps)
                
                # Если середина отрезка не внутри других фигур — рисуем
                mid = ((curr[0] + next_p[0])/2, (curr[1] + next_p[1])/2)
                if not any(is_inside(mid, p) for k, p in enumerate(polygons) if k != i):
                    t.up(); t.goto(curr); t.down(); t.goto(next_p)
    turtle.done()


draw()
