from os import listdir
from os.path import isfile, join, exists
from level_info import path_prefix


def list_files(path):
    if not exists(join(path_prefix, path)):
        return []
    files = [f for f in listdir(join(path_prefix, path)) if isfile(join(path_prefix, path, f))]
    return files
