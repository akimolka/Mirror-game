import pygame
from style import Style


def get_text_size(style, message, size):
    font = pygame.font.SysFont(style.font, size, style.bold, style.italic)
    text = font.render(message, True, style.textcolor)
    return text.get_size()


def calculate_size(dimensions, style, message):
    width = dimensions[0]
    height = dimensions[1]
    precision = 1

    left = 0
    right = 300
    while right - left > precision:
        mid = int((left + right) / 2)
        w, h = get_text_size(style, message, mid)
        if w > float(style.size) * width or h > float(style.size) * height:
            right = mid
        else:
            left = mid
    return right


class Text:
    def __init__(self, pos, dimensions, message, style):
        pygame.font.init()
        size = calculate_size(dimensions, style, message)
        self.font = pygame.font.SysFont(style.font, size, style.bold, style.italic)
        self.text = self.font.render(message, True, style.textcolor)
        self.rect = pygame.Rect(pos, dimensions)
        self.color = style.background

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        textrect = self.text.get_rect()
        textrect.center = self.rect.center
        screen.blit(self.text, textrect)

    def handle_input(self, event):
        pass


class Button:
    def __init__(self, pos, dimensions, message, style, action, motion_action=None):
        self.text = Text(pos, dimensions, message, style)
        self.rect = pygame.Rect(pos, dimensions)
        self.action = action
        self.motion_action = motion_action

    def draw(self, screen):
        self.text.draw(screen)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action()
        if event.type == pygame.MOUSEMOTION and self.rect.collidepoint(event.pos) and self.motion_action:
            self.motion_action()


