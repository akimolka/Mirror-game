import os
import json
from polygon_by_points import polygon_by_points

path_prefix = "../level_info_save_folder/"

if not os.path.exists(path_prefix):
    os.makedirs(path_prefix)


class LevelInfo:
    def __init__(self):
        self.points = [[]]
        self.mirrors = [[]]
        self.start_point = None
        self.finish_segment = []
        self.MIRRORS_WIDTH = 7
        self.attempts = [30, 20, 10]


def read(path, name):
    if not os.path.exists(os.path.join(path_prefix, path)):
        os.makedirs(os.path.join(path_prefix, path))

    file = open(os.path.join(path_prefix, path, name), 'r')
    info = json.loads(file.read())
    file.close()

    res = LevelInfo()
    res.points = info["points"]
    res.start_point = info["start_point"]
    res.finish_segment = info["finish_segment"]
    res.MIRRORS_WIDTH = info["MIRRORS_WIDTH"]
    res.attempts = info["attempts"]
    res.mirrors.clear()
    for point in res.points:
        res.mirrors.append(polygon_by_points(point, res.MIRRORS_WIDTH))

    return res

    
def write(level, path, name):
    info = {
        "points" : level.points,
        # "mirrors" : mirrors,
        "start_point" : level.start_point,
        "finish_segment" : level.finish_segment,
        "MIRRORS_WIDTH" : level.MIRRORS_WIDTH,
        "attempts" : level.attempts
        }

    if not os.path.exists(os.path.join(path_prefix, path)):
        os.makedirs(os.path.join(path_prefix, path))

    file = open(os.path.join(path_prefix, path, name), 'w')
    file.write(json.dumps(info))
    file.close()
