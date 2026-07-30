# TODO create object classes. should function similar to room borders.
from abc import ABC, abstractmethod
import pygame

pygame.init()

class Object(ABC):
    def __init__(self, type, window, x, y, width, height, color):
        self.type = type
        self._window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.remove = False

    def update(self, data):
        pass

    def tick(self, data):
        pass

    def render(self, camera):
        pass