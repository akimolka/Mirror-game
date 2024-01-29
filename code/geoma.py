class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if (self is None) and (other is None):
            return True
        if (self is None) or (other is None):
            return False
        return (other - self).len() < 0.01

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def __mod__(self, other):
        return self.x * other.y - self.y * other.x

    def __truediv__(self, scale):
        return Point(self.x / scale, self.y / scale)

    def len(self):
        return (self.x*self.x + self.y*self.y)**0.5

    def normalize(self, new_len):
        if self.len() == 0:
            return Point(0, new_len)
        factor = self.len() / new_len
        return self / factor

    def rotate90(self):
        return Point(-self.y, self.x)

    def dist_to_line(self, line):
        return (line.direction.y * self.x - line.direction.x * self.y + line.direction % line.start) / line.direction.len()

    def project(line):
        dist = self.dist_to_line(line)
        dir = line.direction.rotate90().normalize(dist)
        return self + dir

    def reflect(self, line):
        dist = self.dist_to_line(line)
        dir = line.direction.rotate90().normalize(2*dist)
        return self + dir




def tuples_to_points(tuple_points):
    res = list();
    for p in tuple_points:
        res.append(Point(p[0], p[1]))
    return res

def points_to_tuples(points):
    res = list();
    for p in points:
        res.append((p.x, p.y))
    return res

def clear_polygon(polygon):
    res = []
    for p in polygon:
        if len(res) == 0:
            res.append(p)
            continue
        if res[-1] == p:
            continue
        if len(res) >= 2:
            if (res[-1] - res[-2]) % (p - res[-1]) == 0:
                res.pop()
        res.append(p)
    return res


class Line:
    def __init__(self, start, direction):
        self.start = start
        self.direction = direction


def line_through(point1, point2):
    return Line(point1, point2-point1);


def intersect(l1, l2):
    x = (l1.direction % l1.start) * l2.direction.x - (l2.direction % l2.start) * l1.direction.x
    y = (l1.direction % l1.start) * l2.direction.y - (l2.direction % l2.start) * l1.direction.y
    return Point(x, y) / (l1.direction % l2.direction)

def line_segment_intersect(line, segment):
    p1 = segment.start
    p2 = p1 + segment.direction
    chr1 = (line.direction % (p1 - line.start))
    chr2 = (line.direction % (p2 - line.start))
    if chr1 * chr2 > 0:
        return None
    if chr1 == 0 and chr2 == 0:
        is_in = (p2 - line.start) * (p1 - line.start) < 0
        is_dir = (line.direction * segment.direction) > 0
        if is_in ^ is_dir:
            return p1
        else:
            return p2
    if chr1 == 0:
        return p1
    if chr2 == 0:
        return p2
    return intersect(line, segment)
    
def ray_segment_intersect(ray, segment):
    res = line_segment_intersect(ray, segment)
    if res is None:
        return None
    if ray.direction * (res-ray.start) < 0:
        return None
    return res

def reflect(ray, segment):
    meet = ray_segment_intersect(ray, segment)
    if meet == None:
        return None
    return line_through(meet, (meet+ray.direction).reflect(segment))

