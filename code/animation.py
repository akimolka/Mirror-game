import pygame
from state import State
import time
from design import *

INTERVAL = 0.25


def draw(screen, animation_data, path):
    shown_segments = animation_data.shown_segments
    if shown_segments == len(path) - 1:
        return

    if shown_segments:
        pygame.draw.lines(screen, TRACK_COLOR, False, path[:shown_segments + 1])
    if shown_segments < len(path) - 1:
        pygame.draw.line(screen, RAY_COLOR, path[shown_segments], path[shown_segments + 1])

    if not animation_data.last_update or time.time() - animation_data.last_update > INTERVAL:
        animation_data.shown_segments += 1
        animation_data.last_update = time.time()
