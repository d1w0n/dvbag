from abc import ABC, abstractmethod
from config import BASE_DIR
import os
import pygame

pygame.init()

class UI(ABC):
    def __init__(self, type, name, window, x = 0, y = 0, width = 0, height = 0, color = (0, 0, 0)):
        self._window = window
        self.type = type
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    @abstractmethod
    def render(self):
        pass

class Bar(UI):
    def __init__(self, name, window, x, y, width, height, color, stat = 100):
        super().__init__("Bar", name, window, x, y, width, height, color)
        self.stat = stat

    def render(self):
        pygame.draw.line(self._window, self.color, (self.x, self.y + self.height / 2), (self.x + self.width * (self.stat / 100), self.y + self.height / 2), self.height)

class Text(UI):
    def __init__(self, name, window, x, y, size, text, color, font = None):
        super().__init__("Bar", name, window, x, y, 0, 0, color)
        self.font = pygame.font.Font(font, size)
        self._text_surface = self.font.render(text, True, self.color)

    def render(self):
        self._window.blit(self._text_surface, (self.x, self.y))

    def set_text(self, text: str):
        self._text_surface = self.font.render(text, True, self.color)
