import pygame
from state import State


def add_point(lst, point):
    if len(lst) == 2:
        lst.pop()
    lst.append(point)


def handle_input(event, state, info, finish_ready):
    finish_segment = info.finish_segment
    if event.type == pygame.MOUSEBUTTONDOWN:
        add_point(finish_segment, event.pos)
        if len(finish_segment) == 2:
            finish_ready = True

    elif event.type == pygame.MOUSEMOTION:
        if not finish_ready and finish_segment:
            add_point(finish_segment, event.pos)

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_u and finish_segment:
            finish_segment.pop()
            finish_ready = False
        if event.key == pygame.K_RETURN and finish_ready:
            state = State.choose_direction
    return state, finish_ready
