# TODO create object classes. should function similar to room borders.
from scripts.instance import Instance
import pygame

pygame.init()

class Object(Instance):
    def __init__(self, type, window, x, y, width, height, color):
        super().__init__(type, "assets/images/placeholder.png", window, x, y, width, height)
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