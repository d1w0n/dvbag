import pygame
import math
from scripts.instance import Instance

pygame.init()

class Particle(Instance):
    def __init__(self, window, x, y, width, height, speed, direction):
        super().__init__("Particle", "assets/placeholder_red.png", window, x, y, width, height)
        self.speed = speed
        self.direction = direction
        self._speed_decay = 0.8

    def update(self, instance_list, room, camera):
        for instance in instance_list:
            if instance.type == "Player":
                if self.get_collision(instance):
                    self.remove = True

        if self.get_room_collision_x(room) or self.get_room_collision_y(room):
            self.remove = True

    def tick(self):
        self.velocity_x = self.speed * math.cos(math.radians(self.direction))
        self.velocity_y = self.speed * math.sin(math.radians(self.direction))
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.speed *= self._speed_decay

    def render(self, camera_x, camera_y):
        self._window.blit(self._sprite, (self.x - self.width / 2 - camera_x, self.y - self.height / 2 - camera_y))