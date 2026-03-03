import turtle
import math

from test_figure import all_tests
SCALE = 2.5
DRAW_SPEED = 3
EPSILON = 1e-5


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
        return (x1 + it1 * (x2 - x1), y1 + it1 * (y2 - y1))
    return None


def is_inside(p, poly):
    x, y = p
    n = len(poly)
    inside = False
    for i in range(n):
        p1x, p1y = poly[i]
        p2x, p2y = poly[(i + 1) % n]
        if ((p1y > y) != (p2y > y)) and \
           (x < (p2x - p1x) * (y - p1y) / (p2y - p1y) + p1x - EPSILON):
            inside = not inside
    return inside


def get_polygon_area(poly):
    area = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        area += (x1 * y2 - x2 * y1)
    return area / 2


def find_loops(segments):
    loops = []
    unused = list(segments)
    while unused:
        current_loop = []
        seg = unused.pop(0)
        p_start, p_end = seg
        current_loop.append(p_start)
        last_p = p_end
        while True:
            found = False
            for i, (s1, s2) in enumerate(unused):
                if math.dist(last_p, s1) < EPSILON:
                    current_loop.append(s1)
                    last_p = s2
                    unused.pop(i)
                    found = True
                    break
                elif math.dist(last_p, s2) < EPSILON:
                    current_loop.append(s2)
                    last_p = s1
                    unused.pop(i)
                    found = True
                    break
            if not found or math.dist(last_p, p_start) < EPSILON:
                break
        loops.append(current_loop)
    return loops


def solve_and_draw(polygons):
    screen = turtle.Screen()
    t = turtle.Turtle()
    t.speed(DRAW_SPEED)

    t.pensize(1)
    t.pencolor("lightgray")
    for poly in polygons:
        t.up()
        t.goto(poly[0][0] * SCALE, poly[0][1] * SCALE)
        t.down()
        for x, y in poly[1:] + [poly[0]]:
            t.goto(x * SCALE, y * SCALE)

    valid_segments = []
    for i, poly in enumerate(polygons):
        for j in range(len(poly)):
            p1, p2 = poly[j], poly[(j + 1) % len(poly)]
            splits = [p1, p2]
            for k, other in enumerate(polygons):
                if i == k:
                    continue
                for m in range(len(other)):
                    inter = get_intersection(
                        p1,
                        p2,
                        other[m],
                        other[(m + 1) % len(other)]
                    )
                    if inter:
                        splits.append(inter)

            splits = sorted(
                list(set(splits)),
                key=lambda p: (p[0]-p1[0])**2 + (p[1]-p1[1])**2
            )
            for s in range(len(splits) - 1):
                start, end = splits[s], splits[s+1]
                mid = ((start[0] + end[0])/2, (start[1] + end[1])/2)
                if not any(
                    is_inside(mid, p) for k, p in enumerate(polygons) if k != i
                ):
                    valid_segments.append((start, end))

    loops = find_loops(valid_segments)

    outer_idx = -1
    min_x = float('inf')
    for idx, loop in enumerate(loops):
        for x, y in loop:
            if x < min_x:
                min_x = x
                outer_idx = idx

    for idx, loop in enumerate(loops):
        is_outer = (idx == outer_idx)
        area = get_polygon_area(loop)

        formatted_coords = [tuple(round(c, 2) for c in p) for p in loop]

        if is_outer:
            if area > 0:
                loop.reverse()
            t.pencolor("red")
            t.pensize(3)
            print(f"Внешний периметр. Координаты:{formatted_coords}")
        else:
            if area < 0:
                loop.reverse()
            t.pencolor("blue")
            t.pensize(2)
            print(f"Найдена дыра. Координаты:"
                  f'{formatted_coords}'
                  )

        t.up()
        t.goto(loop[0][0] * SCALE, loop[0][1] * SCALE)
        t.down()
        for pt in loop[1:] + [loop[0]]:
            t.goto(pt[0] * SCALE, pt[1] * SCALE)

    t.hideturtle()


if __name__ == "__main__":
    for i, test_polygons in enumerate(all_tests):
        print(f"\nЗапуск Теста №{i+1}")
        solve_and_draw(test_polygons)
        print("Нажми ENTER в консоли для следующего теста...")
        input() 
        turtle.clearscreen()
    print("Все тесты пройдены!")
    turtle.bye()
