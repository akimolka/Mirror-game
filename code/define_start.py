import pygame
from state import State


def handle_input(event, state, info):
    if event.type == pygame.MOUSEBUTTONDOWN:
        info.start_point = event.pos
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN and info.start_point:
            state = State.define_finish
    return state
