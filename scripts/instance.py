from abc import ABC, abstractmethod
from config import BASE_DIR
import os
import pygame

pygame.init()

class Instance(ABC):

    @abstractmethod
    def __init__(self, type, sprite = "assets/images/placeholder.png", window = 0, x = 0, y = 0, width = 32, height = 32):
        self.type = type
        self._window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._distance = 0
        self.add_score = 0
        self.set_sprite(sprite)

        self.remove = False
        self.can_pre_update = False

    def pre_update(self, instance_list, room, camera):
        pass
    
    @abstractmethod
    def update(self, instance_list: list, room, camera):
        pass

    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def render(self, camera_x: float, camera_y: float):
        pass

    def get_distance(self, dx, dy):
        return (dx ** 2 + dy ** 2) ** 0.5
    
    def get_velocity(self, dx, dy, speed):
        return (dx / self.get_distance(dx, dy) * speed if dx != 0 or dy != 0 else 0, dy / self.get_distance(dx, dy) * speed if dx != 0 or dy != 0 else 0)
    
    def get_collision(self, other):
        _distance = self.get_distance(self.x - other.x, self.y - other.y)
        return _distance <= self.width / 2 + other.width / 2 or _distance <= self.height / 2 + other.height / 2
    
    def get_room_collision_x(self, room):
        return self.x + self.width / 2 > room.width / 2 or self.x - self.width / 2 < -room.width / 2
    
    def get_room_collision_y(self, room):
        return self.y + self.height / 2 > room.height / 2 or self.y - self.height / 2 < -room.height / 2
    
    def get_out_of_view(self, camera):
        return self.x - self.width / 2 - camera.x + camera.shake_random_x > camera.width or \
        self.x + self.width / 2 - camera.x + camera.shake_random_x < 0 or \
        self.y - self.height / 2 - camera.y + camera.shake_random_y > camera.height or \
        self.y + self.height / 2 - camera.y + camera.shake_random_y < 0
    
    def get_instance_in_range(self, other, range):
        return self.get_distance((other.x + other.width / 2) - (self.x + self.width / 2), (other.y + other.height / 2) - (self.y + self.height / 2)) <= range
    
    def set_sprite(self, file):
        self._sprite = pygame.image.load(os.path.join(BASE_DIR, *file.replace("\\", "/").split("/"))).convert_alpha() # side note: i hate this so much
        self._sprite = pygame.transform.scale(self._sprite, (round(self.width), round(self.height)))

    def tint_surface(surface, color):
        tinted = surface.copy()
        tinted.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        return tinted