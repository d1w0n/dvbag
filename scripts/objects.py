# TODO create object classes. should function similar to room borders.
import pygame

pygame.init()

class Object:
    def __init__(self, window, x, y, width, height, color):
        super().__init__("Object", None, window, x, y, width, height)
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