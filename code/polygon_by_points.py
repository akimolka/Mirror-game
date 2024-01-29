from geoma import *
# import geoma
# import copy

def rectangle(p1, p2, width):
    dir = (p2 - p1).normalize(width/2)
    dir90 = dir.rotate90()
    return [p1+dir90-dir, p2+dir90+dir, p2-dir90+dir, p1-dir90-dir]

def polygon_by_points_main(points, width):
    if len(points) == 0:
        return [];
    if len(points) == 1:
        return rectangle(points[0], points[0], width)

    left = list()
    right = list()

    r = rectangle(points[0], points[1], width)
    left.append(r[0])
    right.append(r[3])

    for ind in range(1, len(points) - 1):
        pr = points[ind - 1]
        me = points[ind]
        nx = points[ind + 1]

        r1 = rectangle(pr, me, width)
        r2 = rectangle(me, nx, width)

        left.append(intersect(line_through(r1[0], r1[1]), line_through(r2[0], r2[1])))
        right.append(intersect(line_through(r1[3], r1[2]), line_through(r2[3], r2[2])))
        
    r = rectangle(points[-2], points[-1], width)
    left.append(r[1])
    right.append(r[2])

    right.reverse()
    return left + right

def polygon_by_points(tuple_points, width):
    return points_to_tuples(polygon_by_points_main(clear_polygon(tuples_to_points(tuple_points)), width))
