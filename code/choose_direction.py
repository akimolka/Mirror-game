import pygame
from state import State
import reflection_calculator
from random import randint


def visible_path(start_point, target, cnt_reflections, mirrors, width, height):
    return reflection_calculator.calculate_visible_path(start_point, target, cnt_reflections, mirrors, width, height)


def all_path(start_point, target, mirrors, width, height, finish_segment):
    return reflection_calculator.calculate_real_path(start_point, target, mirrors, width, height, finish_segment)


def handle_input(event, state, player, target):
    if event.type == pygame.MOUSEMOTION:
        target = event.pos
    if event.type == pygame.KEYDOWN:
        if event.unicode.isdigit():
            player.cnt_reflections = int(event.unicode)
        if event.key == pygame.K_RETURN and target:
            player.attempts += 1
            state = State.animation
    return state, target
