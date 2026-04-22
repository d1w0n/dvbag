import pygame
import random
from scripts.instance import Instance

pygame.init()

class Particle(Instance):
    def __init__(self, window, x, y, width, height, speed, target_x, target_y):
        super().__init__("Particle", "assets/placeholder_red.png", window, x, y, width, height)
        self.speed = speed
        self._dx = target_x - self.x
        self._dy = target_y - self.y
        self._magnitude = self.get_magnitude(self._dx, self._dy)
        self.x_velocity = self._dx / self._magnitude * self.speed
        self.y_velocity = self._dy / self._magnitude * self.speed

    def update(self, instance_list, room, camera):
        self._room_width = room.width
        self._room_height = room.height
        if self.get_room_collision_x() or self.get_room_collision_y():
            self.remove = True

    def tick(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def render(self, camera_x, camera_y):
        self._window.blit(self._sprite, (self.x - self.width / 2 - camera_x, self.y - self.height / 2 - camera_y))