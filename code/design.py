from pygame.color import THECOLORS

START_RADIUS = 5
FINISH_WIDTH = 4

START_COLOR = (0, 255, 0)
COLORS = [THECOLORS["red"], THECOLORS["orange"], THECOLORS["yellow"], THECOLORS["green"], THECOLORS["purple"]]
FINISH_COLOR = (0, 255, 0)
MIRRORS_COLOR = (0, 0, 255)
RAY_COLOR = (255, 255, 255)
TRACK_COLOR = (100, 100, 100)


def mute_color(color):
    value = 3
    return color[0] / value, color[1] / value, color[2] / value
