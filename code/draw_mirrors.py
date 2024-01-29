import pygame
from state import State
from polygon_by_points import polygon_by_points


def calculate_mirrors(points, width):
    return polygon_by_points(points, width)


def handle_input(event, state, info):
    last_points = info.points[-1]
    last_mirrors = info.mirrors[-1]

    if event.type == pygame.MOUSEBUTTONDOWN:
        last_points.append(event.pos)
        last_mirrors[:] = calculate_mirrors(last_points, info.MIRRORS_WIDTH)
    elif event.type == pygame.MOUSEMOTION:
        last_points.append(event.pos)
        last_mirrors[:] = calculate_mirrors(last_points, info.MIRRORS_WIDTH)
        last_points.pop()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_u:
            if last_points:
                last_points.pop()
                last_mirrors[:] = calculate_mirrors(last_points, info.MIRRORS_WIDTH)
            elif len(info.points) >= 2:
                info.points.pop()
                info.mirrors.pop()
        if event.key == pygame.K_RETURN:
            if not last_points:
                info.points.pop()
                info.mirrors.pop()
            last_mirrors[:] = calculate_mirrors(last_points, info.MIRRORS_WIDTH)
            state = State.define_start
        if event.key == pygame.K_SPACE:
            last_mirrors[:] = calculate_mirrors(last_points, info.MIRRORS_WIDTH)
            if last_points:
                info.points.append([])
                info.mirrors.append([])
    return state
