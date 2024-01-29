from state import State
import choose_direction
import animation
import pygame
from level_info import LevelInfo
from design import *
import random
from button import Text
from style import Style


class Player:
    def __init__(self, start_point):
        self.current_point = start_point
        self.cnt_reflections = 2
        self.color = random.choice(COLORS)
        self.attempts = 0


class AnimationHelper:
    shown_segments = 0
    last_update = None


def change_turn(win, active_player, players):
    if win:
        return State.victory, active_player
    else:
        return State.choose_direction, (active_player + 1) % players


class Level:
    def __init__(self, dimensions, players=1, info=LevelInfo(), widgets=None):
        if widgets is None:
            self.widgets = []
        else:
            self.widgets = widgets
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.info = info
        self.state = State.choose_direction

        self.players = [Player(info.start_point) for i in range(players)]
        self.active_player = 0
        self.target = None
        self.path = []
        self.animation_data = AnimationHelper()
        self.win = False

    def clear_visual_data(self):
        self.target = None
        self.path = []
        self.animation_data = AnimationHelper()

    def restart(self):
        self.clear_visual_data()
        self.win = False
        for player in self.players:
            player.current_point = self.info.start_point
            player.attempts = 0

    def handle_input(self, event):
        for widget in self.widgets:
            widget.handle_input(event)

        player = self.players[self.active_player]
        if self.state == State.choose_direction:
            self.state, self.target = choose_direction.handle_input(event, self.state, player, self.target)
            if self.target:
                self.path = choose_direction.visible_path(player.current_point, self.target,
                                                          player.cnt_reflections, self.info.mirrors,
                                                          self.width, self.height)
        if self.state == State.animation and not self.animation_data.shown_segments:
            self.path, self.win = choose_direction.all_path(player.current_point, self.target,
                                                            self.info.mirrors,
                                                            self.width, self.height, self.info.finish_segment)
        if self.state == State.victory:
            if event.type == pygame.KEYDOWN:
                self.restart()
                self.active_player = (self.active_player + 1) % len(self.players)
                self.state = State.choose_direction

    def __assemble_counters__(self, screen):
        width = screen.get_width()
        height = screen.get_height()
        counter_width = width / 30
        counter_height = height / 20
        counters = []
        cnt = len(self.info.attempts)
        for i in range(cnt):
            counters.append(Text(
                (width - counter_width * (cnt - i) + 1, 0), (counter_width, counter_height),
                str(max(self.info.attempts[i] - self.players[0].attempts, 0)), Style.Standard
            ))
        return counters

    def __assemble_victory_message__(self, screen):
        width = screen.get_width()
        height = screen.get_height()
        message_width = width / 3
        message_height = height / 3
        if len(self.players) == 1:
            stars = 0
            cnt = len(self.info.attempts)
            for i in range(cnt):
                if self.info.attempts[i] >= self.players[self.active_player].attempts:
                    stars = i + 1
            return Text((width / 3, height / 3), (message_width, message_height),
                        f"You have won {stars} stars!", Style.Standard)
        else:
            return Text((width / 3, height / 3), (message_width, message_height),
                        f"You have won! Score: {self.players[self.active_player].attempts}", Style.Standard)

    def draw(self, screen):
        if len(self.players) == 1:
            initial_len = len(self.widgets)
            self.widgets += self.__assemble_counters__(screen)
        for widget in self.widgets:
            widget.draw(screen)
        if len(self.players) == 1:
            while len(self.widgets) > initial_len:
                self.widgets.pop()

        for mirror in self.info.mirrors:
            pygame.draw.polygon(screen, MIRRORS_COLOR, mirror)
        for index, player in enumerate(self.players):
            # color = START_COLOR if index == self.active_player else OTHERS_COLOR
            color = player.color if index == self.active_player else mute_color(player.color)
            pygame.draw.circle(screen, color, player.current_point, START_RADIUS)
        pygame.draw.line(screen, FINISH_COLOR, *self.info.finish_segment, FINISH_WIDTH)

        if self.state == State.choose_direction and len(self.path) >= 2:
            pygame.draw.lines(screen, RAY_COLOR, False, self.path)

        if self.state == State.animation:
            animation.draw(screen, self.animation_data, self.path)
            if self.animation_data.shown_segments == len(self.path) - 1:
                self.players[self.active_player].current_point = self.path[-1]
                self.state, self.active_player = change_turn(self.win, self.active_player,
                                                             len(self.players))
                self.clear_visual_data()
        if self.state == State.victory:
            victory_message = self.__assemble_victory_message__(screen)
            victory_message.draw(screen)
