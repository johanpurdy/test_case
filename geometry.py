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


def draw_clean_outline(polygons):
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()

    # 1. Фоновая отрисовка (серый)
    t.pencolor("lightgray")
    for poly in polygons:
        t.up()
        t.goto(poly[0]) 
        t.down()
        for p in poly[1:] + [poly[0]]:
            t.goto(p)

    # 2. Поиск и отрисовка внешнего контура (красный)
    t.pencolor("red")
    t.pensize(3)
    valid_segments = []

    for i, poly in enumerate(polygons):
        for j in range(len(poly)):
            p1, p2 = poly[j], poly[(j + 1) % len(poly)]
            splits = [p1, p2]
            for k, other_poly in enumerate(polygons):
                if i == k:
                    continue
                for m in range(len(other_poly)):
                    p3, p4 = (
                        other_poly[m],
                        other_poly[(m + 1) % len(other_poly)]
                    )
                    inter = get_intersection(p1, p2, p3, p4)
                    if inter:
                        splits.append(inter)

            # Сортируем точки вдоль линии p1 -> p2
            splits = sorted(
                list(set(splits)),
                key=lambda p:
                (p[0]-p1[0])**2 + (p[1]-p1[1])**2
            )

            # Проверяем каждый кусок между точками разрыва
            for s in range(len(splits) - 1):
                start, end = splits[s], splits[s+1]
                mid = ((start[0] + end[0])/2, (start[1] + end[1])/2)
                
                # Если середина отрезка не внутри других фигур — рисуем и сохраняем
                if not any(is_inside(mid, p) for k, p in enumerate(polygons) if k != i):
                    valid_segments.append((start, end))
                    t.up()
                    t.goto(start)
                    t.down()
                    t.goto(end)

    # Собираем итоговый список точек через list comprehension
    result = list(dict.fromkeys([pt for seg in valid_segments for pt in seg]))
    return result

# Пример данных
squares = [
    [(-100, -100), (100, -100), (100, 100), (-100, 100)],
    [(0, 0), (150, 0), (150, 150), (0, 150)]
]
triangels = [
    [(0, 0), (100, 0), (100, 100), (0, 100)],
    [(50, 50), (150, 50), (150, 150), (50, 150)],
    [(80, -20), (180, -20), (130, 80)]
]

final_points = draw_clean_outline(triangels)
print("Итоговые точки контура:", final_points)
turtle.done()