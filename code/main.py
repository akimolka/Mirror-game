import sys
import pygame
from datetime import datetime  # for debug

import level_info
from menu import Menu
from style import Style
from button import Button
from preview import Preview
from level_construction import LevelConstruction
from level import Level
from level_info import LevelInfo
from list_files import list_files
import math


def get_grid(cnt):
    column = max(1, int(cnt**0.5))
    row = math.ceil(cnt / column)
    return row, column


def pos_and_dimensions_gen(cnt, dimensions):
    width = dimensions[0]
    height = dimensions[1]
    row_cnt, column_cnt = get_grid(cnt)
    row_parts = row_cnt * 2 + 1
    level_width = width / row_parts
    level_height = level_width * height / width
    space_height = (height - level_height * column_cnt) / (column_cnt + 1)

    for j in range(column_cnt):
        for i in range(row_cnt):
            if j * row_cnt + i + 1 > cnt:
                return
            width_indent = width * (i * 2 + 1) / row_parts
            height_indent = (j + 1) * space_height + j * level_height
            yield (width_indent, height_indent), (level_width, level_height)


def __assemble_button_back__(dimensions, action):
    width = dimensions[0]
    height = dimensions[1]
    return Button((0, 0), (width / 20, height / 20), "back", Style.Standard, action)


class Game:
    def change_to_1player_menu(self, info=LevelInfo()):
        self.active_page = "1player_menu"

    def change_to_2players_menu(self, info=LevelInfo()):
        self.pages["2players_menu"] = self.__assemble_2players_menu__(self.screen.get_size(), "2players")
        self.active_page = "2players_menu"

    def change_to_level_construction(self, info=LevelInfo()):
        self.active_page = "level_construction"

    def change_to_1p_level(self, info):
        self.active_page = "level"
        button_back = __assemble_button_back__(self.screen.get_size(), self.change_to_1player_menu)
        self.pages["level"] = Level(self.screen.get_size(), 1, info, widgets=[button_back])

    def change_to_2p_level(self, info):
        self.active_page = "level"
        button_back = __assemble_button_back__(self.screen.get_size(), self.change_to_2players_menu)
        self.pages["level"] = Level(self.screen.get_size(), 2, info, widgets=[button_back])

    def exit(self, info=LevelInfo()):
        sys.exit()

    def change_to_main_menu(self, info=LevelInfo()):
        self.active_page = "main_menu"

    def hello(self):
        print("Hello!")

    def __assemble_main_menu__(self, dimensions):
        width = dimensions[0]
        height = dimensions[1]
        button_w = width / 3
        button_h = height / 5
        button_1p = Button((width / 3, height / 5), (button_w, button_h), "1 player", Style.Standard,
                           self.change_to_1player_menu)
        button_2p = Button((width / 3, height * 3 / 5), (button_w, button_h), "2 players", Style.Standard,
                           self.change_to_2players_menu)
        return Menu([button_1p, button_2p])

    def __assemble_1player_menu__(self, dimensions, levels_path):
        files = list_files(levels_path)
        cnt = len(files)
        widgets = []

        pos_and_dim = pos_and_dimensions_gen(cnt, dimensions)
        for index, (pos, dim) in enumerate(pos_and_dim):
            info = level_info.read(levels_path, files[index])
            widgets.append(Preview(pos, dim, info, self.change_to_1p_level))
        button_back = __assemble_button_back__(dimensions, self.change_to_main_menu)
        return Menu(widgets + [button_back])

    def __assemble_2players_menu__(self, dimensions, levels_path):
        files = list_files(levels_path)
        cnt = len(files) + 1
        widgets = []

        pos_and_dim = pos_and_dimensions_gen(cnt, dimensions)
        for index, (pos, dim) in enumerate(pos_and_dim):
            if index == cnt - 1:
                widgets.append(Button(pos, dim, "new", Style.Standard, self.change_to_level_construction))
            else:
                info = level_info.read(levels_path, files[index])
                widgets.append(Preview(pos, dim, info, self.change_to_2p_level))

        button_back = __assemble_button_back__(dimensions, self.change_to_main_menu)
        return Menu(widgets + [button_back])

    def __assemble_level_construction__(self, dimensions):
        button_back = __assemble_button_back__(dimensions, self.change_to_2players_menu)
        return LevelConstruction(self.change_to_2players_menu, keep_log=True, path="2players", widgets=[button_back])

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.pages = dict()
        self.active_page = "main_menu"
        self.pages["main_menu"] = self.__assemble_main_menu__(self.screen.get_size())
        self.pages["1player_menu"] = self.__assemble_1player_menu__(self.screen.get_size(), "1player")
        self.pages["2players_menu"] = self.__assemble_2players_menu__(self.screen.get_size(), "2players")
        self.pages["level_construction"] = self.__assemble_level_construction__(self.screen.get_size())

    def cycle(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                self.pages[self.active_page].handle_input(event)

            self.pages[self.active_page].draw(self.screen)
            pygame.display.flip()
            self.screen.fill((0, 0, 0))
            # print(datetime.now(), state)
            clock.tick(10)

    def start(self):
        self.cycle()

    def __create_level__(self):
        self.active_page = "level_construction"
        self.pages["level_construction"] = LevelConstruction(self.exit, keep_log=True, path="Experiment")
        self.cycle()


game = Game()
game.start()
