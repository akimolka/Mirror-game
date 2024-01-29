import pygame
from state import State
from level_info import LevelInfo
import level_info
import draw_mirrors
import define_start
import define_finish
from design import *
from datetime import datetime


class LevelConstruction:
    def __init__(self, activate_next_page, info=LevelInfo(), keep_log=False, path="mixed", widgets=None):
        if widgets is None:
            self.widgets = []
        else:
            self.widgets = widgets
        self.info = info
        self.state = State.draw_mirrors
        self.keep_log = keep_log
        self.path = path
        self.activate_next_page = activate_next_page
        self.finish_ready = False

    def handle_input(self, event):
        for widget in self.widgets:
            widget.handle_input(event)

        if self.state == State.draw_mirrors:
            self.state = draw_mirrors.handle_input(event, self.state, self.info)
        elif self.state == State.define_start:
            self.state = define_start.handle_input(event, self.state, self.info)
        elif self.state == State.define_finish:
            self.state, self.finish_ready = \
                define_finish.handle_input(event, self.state, self.info, self.finish_ready)
        elif self.state == State.choose_direction:
            if self.keep_log:
                level_info.write(self.info, self.path, str(datetime.now()))
            self.activate_next_page(self.info)

    def draw(self, screen):
        for widget in self.widgets:
            widget.draw(screen)

        for mirror in self.info.mirrors:
            if len(mirror) >= 3:
                pygame.draw.polygon(screen, MIRRORS_COLOR, mirror)
        if self.info.start_point:
            pygame.draw.circle(screen, START_COLOR, self.info.start_point, START_RADIUS)
        if len(self.info.finish_segment) == 2:
            pygame.draw.line(screen, FINISH_COLOR, *self.info.finish_segment, FINISH_WIDTH)

