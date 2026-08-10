# TODO create object classes. should function similar to room borders.
from abc import ABC
import pygame

pygame.init()

class Object(ABC):
    def __init__(self, window, x, y, width, height, color):
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
        pygame.draw.line(self._window, self.color, (-self.width / 2 - camera.x + camera.shake_x, -self.height / 2 - camera.y + camera.shake_y), (self.width / 2 - camera.x + camera.shake_x, -self.height / 2 - camera.y + camera.shake_y), 5)
        pygame.draw.line(self._window, self.color, (self.width / 2 - camera.x + camera.shake_x, -self.height / 2 - camera.y + camera.shake_y), (self.width / 2 - camera.x + camera.shake_x, self.height / 2 - camera.y + camera.shake_y), 5)
        pygame.draw.line(self._window, self.color, (self.width / 2 - camera.x + camera.shake_x, self.height / 2 - camera.y + camera.shake_y), (-self.width / 2 - camera.x + camera.shake_x, self.height / 2 - camera.y + camera.shake_y), 5)
        pygame.draw.line(self._window, self.color, (-self.width / 2 - camera.x + camera.shake_x, self.height / 2 - camera.y + camera.shake_y), (-self.width / 2 - camera.x + camera.shake_x, -self.height / 2 - camera.y + camera.shake_y), 5)

class Wall(Object):
    def __init__(self, window, x, y, width, height):
        super().__init__(window, x, y, width, height, (200, 200, 200))