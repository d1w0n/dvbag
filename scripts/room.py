import pygame

pygame.init()

class Room():
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def render(self, window, color, camera):
        pygame.draw.line(window, color, (-self.width / 2 - camera.x + camera.shake_x, -self.height / 2 - camera.y + camera.shake_y), (self.width / 2 - camera.x + camera.shake_x, -self.height / 2 - camera.y + camera.shake_y), 5)
        # top border.

        pygame.draw.line(window, color, (self.width / 2 - camera.x + camera.shake_x, -self.height / 2 - camera.y + camera.shake_y), (self.width / 2 - camera.x + camera.shake_x, self.height / 2 - camera.y + camera.shake_y), 5)
        # right border.

        pygame.draw.line(window, color, (self.width / 2 - camera.x + camera.shake_x, self.height / 2 - camera.y + camera.shake_y), (-self.width / 2 - camera.x + camera.shake_x, self.height / 2 - camera.y + camera.shake_y), 5)
        # bottom border.

        pygame.draw.line(window, color, (-self.width / 2 - camera.x + camera.shake_x, self.height / 2 - camera.y + camera.shake_y), (-self.width / 2 - camera.x + camera.shake_x, -self.height / 2 - camera.y + camera.shake_y), 5)
        # left border.

        pygame.draw.circle(window, color, (-camera.x + camera.shake_x, -camera.y + camera.shake_y), 3)
        # origin indicator (remove soon). 