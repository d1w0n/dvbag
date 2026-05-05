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
        self.remove = False

    @abstractmethod
    def render(self, offset_x, offset_y):
        pass

class Bar(UI):
    def __init__(self, name, window, x, y, width, height, color, stat = 100):
        super().__init__("Bar", name, window, x, y, width, height, color)
        self.stat = stat

    def render(self):
        pygame.draw.line(self._window, self.color, (self.x, self.y + self.height / 2), (self.x + self.width * (self.stat / 100), self.y + self.height / 2), self.height)



class Text(UI):
    def __init__(self, name, window, x, y, size, text, color, font = None):
        super().__init__("Text", name, window, x, y, 0, 0, color)
        self.font = pygame.font.Font(font, size)
        self._text_surface = self.font.render(text, True, self.color)

    def render(self):
        self._window.blit(self._text_surface, (self.x, self.y))

    def set_text(self, text: str):
        self._text_surface = self.font.render(text, True, self.color)



class TextParticle(Text):
    def __init__(self, name, window, x, y, size, text, color, font = None, duration = 0, x_velocity = 0, y_velocity = 0):
        super().__init__(name, window, x, y, size, text, color, font)
        self.duration = duration
        self._init_ticks = pygame.time.get_ticks()
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

    def render(self):
        if (pygame.time.get_ticks() - self._init_ticks) > self.duration:
            self.remove = True
            pass
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.x_velocity *= 0.9
        self.y_velocity *= 0.9
        self._text_surface.set_alpha(255 - round(255 * ((pygame.time.get_ticks() - self._init_ticks) / self.duration)))
        self._window.blit(self._text_surface, (self.x, self.y))