import turtle
import random
import math


DRAW_SPEED = 15
EPSILON = 1e-5


def generate_random_poly(
        cx,
        cy,
        min_radius=30,
        max_radius=60,
        num_vertices=None
):
    if num_vertices is None:
        num_vertices = random.randint(3, 8)

    angles = sorted(
        [random.uniform(0, 2 * math.pi) for _ in range(num_vertices)]
    )

    poly = []
    for angle in angles:
        r = random.uniform(min_radius, max_radius)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        poly.append((round(x, 1), round(y, 1)))

    return poly


def generate_complex_test_scene(num_figures=3):
    all_polygons = []
    for _ in range(num_figures):
        cx = random.randint(-30, 30)
        cy = random.randint(-20, 20)

        poly = generate_random_poly(cx, cy)
        all_polygons.append(poly)
    return all_polygons


def get_intersection(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    det = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if abs(det) < EPSILON:
        return None
    it1 = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / det
    it2 = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / det
    if 0 <= it1 <= 1 and 0 <= it2 <= 1:
        return (round(x1 + it1 * (x2 - x1), 4), round(y1 + it1 * (y2 - y1), 4))
    return None


def is_inside(p, poly):
    x, y = p
    n = len(poly)
    inside = False
    for i in range(n):
        p1x, p1y = poly[i]
        p2x, p2y = poly[(i + 1) % n]
        if ((p1y > y) != (p2y > y)) and \
           (x < (p2x - p1x) * (y - p1y) / (p2y - p1y + 1e-10) + p1x):
            inside = not inside
    return inside


def get_polygon_area(poly):
    area = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        area += (x1 * y2 - x2 * y1)
    return area / 2


def get_bounds(polygons):
    all_points = [pt for poly in polygons for pt in poly]
    if not all_points:
        return -100, 100, -100, 100
    xs = [p[0] for p in all_points]
    ys = [p[1] for p in all_points]

    return min(xs), max(xs), min(ys), max(ys)


def solve_and_draw(polygons):
    screen = turtle.Screen()
    min_x, max_x, min_y, max_y = get_bounds(polygons)
    margin = 20

    screen.setworldcoordinates(
        min_x - margin,
        min_y - margin,
        max_x + margin,
        max_y + margin
    )

    t = turtle.Turtle()
    t.speed(DRAW_SPEED)

    t.pencolor("lightgray")
    for poly in polygons:
        t.up()
        t.goto(poly[0][0], poly[0][1])
        t.down()
        for x, y in poly[1:] + [poly[0]]:
            t.goto(x, y)

    valid_segments = []
    for i, poly in enumerate(polygons):
        for j in range(len(poly)):
            p1, p2 = poly[j], poly[(j + 1) % len(poly)]
            p1, p2 = (
                round(p1[0], 4), round(p1[1], 4)
            ), (round(p2[0], 4), round(p2[1], 4))

            splits = {p1, p2}
            for k, other in enumerate(polygons):
                if i == k:
                    continue
                for m in range(len(other)):
                    inter = get_intersection(
                        p1, p2, other[m], other[(m + 1) % len(other)]
                    )
                    if inter:
                        splits.add(inter)

            sorted_splits = sorted(
                list(splits), key=lambda p: (p[0]-p1[0])**2 + (p[1]-p1[1])**2
            )

            for s in range(len(sorted_splits) - 1):
                start, end = sorted_splits[s], sorted_splits[s+1]
                mid = ((start[0] + end[0])/2, (start[1] + end[1])/2)
                if not any(
                    is_inside(mid, p) for k, p in enumerate(polygons) if k != i
                ):
                    valid_segments.append((start, end))

    unused = list(valid_segments)
    if not unused:
        return

    loop = []
    seg = unused.pop(0)
    loop.append(seg[0])
    last_p = seg[1]

    while unused:
        found = False
        for i, (s1, s2) in enumerate(unused):
            if math.dist(last_p, s1) < EPSILON:
                loop.append(s1)
                last_p = s2
                unused.pop(i)
                found = True
                break
            elif math.dist(last_p, s2) < EPSILON:
                loop.append(s2)
                last_p = s1
                unused.pop(i)
                found = True
                break
        if not found:
            break

    area = get_polygon_area(loop)
    if area > 0:
        loop.reverse()

    t.pencolor("red")
    t.pensize(3)
    t.up()
    t.goto(loop[0][0], loop[0][1])
    t.down()
    for pt in loop[1:] + [loop[0]]:
        t.goto(pt[0], pt[1])

    t.hideturtle()
    print(
        f"Внешний периметр отрисован. Вершин: {len(loop)}"
        f'Все вершины: {loop}'
    )


if __name__ == "__main__":
    for i in range(10):
        print(f"\nТест №{i+1}")

        test_polygons = generate_complex_test_scene(
            num_figures=100
        )

        solve_and_draw(test_polygons)

        print("Нажми ENTER для следующей генерации...")
        input()
        turtle.clearscreen()
    turtle.bye()
