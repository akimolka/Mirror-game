from geoma import *

def calculate_reflection(ray, reflect_segments, stop_segments):
    segments = [reflect_segments, stop_segments]
    closest = None
    distance = 1e9
    indeces = []
    for rs in range(len(segments)):
        for i in range(len(segments[rs])):
            p = ray_segment_intersect(ray, segments[rs][i])
            if p is None:
                continue
            if p == closest:
                indeces.append((rs, i))
                continue
            if (p - ray.start) == Point(0, 0):
                continue
            if closest == None or distance > (p - ray.start).len():
                closest = p;
                distance = (p - ray.start).len()
                indeces = [(rs, i)]
    if len(indeces) == 0:
        return None
    if len(indeces) == 1:
        return (reflect(ray, segments[indeces[0][0]][indeces[0][1]]), indeces[0])
    return (reflect(ray, segments[indeces[0][0]][indeces[0][1]]), indeces[0])



def calculate_path_main(ray, cnt, reflect_segments, stop_segments, add_path=True, cnt_finish=0):
    res = [ray.start]

    for i in range(cnt):
        ref = calculate_reflection(ray, reflect_segments, stop_segments)
        res.append(ref[0].start)
        if (ref[1][0] == 1):
            return (res, ref[1][1] < cnt_finish)
        if add_path:
            stop_segments.append(line_through(res[-2], res[-1]))
        ray = ref[0]
    ref = calculate_reflection(ray, reflect_segments, stop_segments)
    res.append((res[-1] + ref[0].start) / 2)
    return (res, False)

def converte_and_calculate(start, target, cnt, polygons, width, height, mode, finish = None):
    reflect_segments = []
    stop_segments = []
    for tuple_polygon in polygons:
        polygon = tuples_to_points(tuple_polygon)
        for i in range(len(polygon)):
            reflect_segments.append(line_through(polygon[i], polygon[(i + 1) % len(polygon)]))
    reflect_segments.append(line_through(Point(0, 0), Point(width, 0)))
    reflect_segments.append(line_through(Point(width, 0), Point(width, height)))
    reflect_segments.append(line_through(Point(width, height), Point(0, height)))
    reflect_segments.append(line_through(Point(0, height), Point(0, 0)))
    st = tuples_to_points([start, target])
    ray = line_through(st[0], st[1])

    if mode == 'visible':
        res = calculate_path_main(ray, cnt, reflect_segments, stop_segments, False)
        return points_to_tuples(res[0])
    
    if mode == 'real':
        st = tuples_to_points(finish)
        stop_segments = [line_through(st[0], st[1])] + stop_segments
        res = calculate_path_main(ray, cnt, reflect_segments, stop_segments, True, 1)
        return (points_to_tuples(res[0]), res[1])

def calculate_visible_path(start, target, cnt, polygons, width, height):
    return converte_and_calculate(start, target, cnt, polygons, width, height, 'visible')

def calculate_real_path(start, target, polygons, width, height, finish):
    return converte_and_calculate(start, target, 100, polygons, width, height, 'real', finish)


# print(calculate_real_path((3, 3), (4, 4), [[(2, 5), (6, 5), (4, 7)]], 11, 9, ((9, 0), (11, 2))))


