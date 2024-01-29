import pygame
from design import *


def scale(ratio, point):
    return point[0] * ratio, point[1] * ratio


def scale_and_move(pos, ratio, point):
    point = scale(ratio, point)
    return pos[0] + point[0], pos[1] + point[1]


def scale_and_move_list(pos, ratio, lst):
    new_lst = []
    for point in lst:
        new_lst.append(scale_and_move(pos, ratio, point))
    return new_lst


class Preview:
    def __init__(self, pos, dimensions, info, activate_level):
        self.pos = pos
        self.dimensions = dimensions
        self.info = info
        self.activate_level = activate_level
        self.rect = pygame.Rect(pos, dimensions)

    def draw(self, screen):
        ratio = self.dimensions[0] / screen.get_width()

        mirror_width = max(1, int(ratio * self.info.MIRRORS_WIDTH))
        mirror_point_radius = max(1, int(ratio * self.info.MIRRORS_WIDTH / 2))
        start_radius = max(1, int(ratio * START_RADIUS))
        finish_width = max(1, int(ratio * FINISH_WIDTH))

        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        for mirror in self.info.points:
            mirror = scale_and_move_list(self.pos, ratio, mirror)
            if len(mirror) >= 2:
                pygame.draw.lines(screen, MIRRORS_COLOR, False, mirror, mirror_width)
            else:
                pygame.draw.circle(screen, MIRRORS_COLOR, mirror[0], mirror_point_radius)
        if self.info.start_point:
            start_point = scale_and_move(self.pos, ratio, self.info.start_point)
            pygame.draw.circle(screen, START_COLOR, start_point, start_radius)
        if len(self.info.finish_segment) == 2:
            finish_segment = scale_and_move_list(self.pos, ratio, self.info.finish_segment)
            pygame.draw.line(screen, FINISH_COLOR, *finish_segment, finish_width)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.activate_level(self.info)
