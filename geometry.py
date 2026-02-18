import ast
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

    t.pencolor("lightgray")
    for poly in polygons:
        t.up()
        t.goto(poly[0])
        t.down()
        for p in poly[1:] + [poly[0]]:
            t.goto(p)

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

            splits = sorted(
                list(set(splits)),
                key=lambda p:
                (p[0]-p1[0])**2 + (p[1]-p1[1])**2
            )

            for s in range(len(splits) - 1):
                start, end = splits[s], splits[s+1]
                mid = ((start[0] + end[0])/2, (start[1] + end[1])/2)

                if not any(is_inside(mid, p) for k, p in enumerate(polygons) if k != i):
                    valid_segments.append((start, end))
                    t.up()
                    t.goto(start)
                    t.down()
                    t.goto(end)

    result = list(dict.fromkeys([pt for seg in valid_segments for pt in seg]))
    return result


def get_input_polygons():
    count = int(input("Сколько фигур будет? "))
    polygons = []
    print(f"Введите {count} список(а) координат в формате [(x1, y1), (x2, y2), ...]:")
    for i in range(count):
        raw_data = input(f"Фигура {i+1}: ")
        poly = ast.literal_eval(raw_data)
        polygons.append(poly)
    return polygons


test1 = [
    [(0, 0), (100, 0), (100, 100), (0, 100)],
    [(40, -20), (60, -20), (60, 120), (40, 120)]
]

test2 = [
    [(0, 0), (150, 0), (150, 100), (0, 100)],
    [(50, -20), (70, -20), (70, 120), (50, 120)],
    [(100, -20), (120, -20), (120, 120), (100, 120)]
]

test3 = [
    [(0, 0), (100, 0), (100, 100), (0, 100)],
    [(20, 20), (80, 20), (80, 80), (20, 80)],
    [(40, 40), (60, 40), (60, 60), (40, 60)]
]

test4 = [
    [(0, 40), (200, 40), (200, 60), (0, 60)],
    [(0, 80), (200, 80), (200, 100), (0, 100)],
    [(40, 0), (60, 0), (60, 200), (40, 200)],
    [(120, 0), (140, 0), (140, 200), (120, 200)]
]

test5 = [
    [(0, 0), (100, 0), (100, 100), (0, 100)],
    [(50, 50), (150, 50), (150, 150), (50, 150)],
    [(100, 100), (200, 100), (200, 200), (100, 200)]
]

test6 = [
    [(0, 0), (40, 0), (40, 40), (0, 40)],
    [(30, 30), (70, 30), (70, 70), (30, 70)],
    [(60, 60), (100, 60), (100, 100), (60, 100)],
    [(15, 15), (55, 15), (55, 55), (15, 55)],
    [(45, 45), (85, 45), (85, 85), (45, 85)]
]

test7 = [
    [(0, 50), (200, 50), (200, 70), (0, 70)],
    [(80, 0), (120, 0), (120, 150), (80, 150)]
]

test8 = [
    [(0, 0), (200, 0), (200, 150), (0, 150)],
    [(20, 20), (180, 20), (180, 130), (20, 130)],
    [(20, 20), (60, 20), (60, 60), (20, 60)],
    [(140, 90), (180, 90), (180, 130), (140, 130)]
]


polygons = #test
final_points = draw_clean_outline(polygons)
print(f"Итоговых точек: {len(final_points)}")
turtle.done()