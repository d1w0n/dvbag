import pygame

pygame.init()

class Room:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, window, color, camera_x, camera_y):
        pygame.draw.line(window, color, (-self.width / 2 - camera_x, -self.height / 2 - camera_y), (self.width / 2 - camera_x, -self.height / 2 - camera_y), 5)
        # top border.

        pygame.draw.line(window, color, (self.width / 2 - camera_x, -self.height / 2 - camera_y), (self.width / 2 - camera_x, self.height / 2 - camera_y), 5)
        # right border.

        pygame.draw.line(window, color, (self.width / 2 - camera_x, self.height / 2 - camera_y), (-self.width / 2 - camera_x, self.height / 2 - camera_y), 5)
        # bottom border.

        pygame.draw.line(window, color, (-self.width / 2 - camera_x, self.height / 2 - camera_y), (-self.width / 2 - camera_x, -self.height / 2 - camera_y), 5)
        # left border.

        pygame.draw.circle(window, color, (-camera_x, -camera_y), 3)
        # origin indicator. 