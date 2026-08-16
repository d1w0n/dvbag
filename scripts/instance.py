from abc import ABC, abstractmethod
import os
import pygame
from config import BASE_DIR

pygame.init()

class Instance(ABC):

    @abstractmethod
    def __init__(self, type, sprite, window, x, y, width, height):
        self.type = type
        self._window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if isinstance(sprite, str):
            self.set_sprite(sprite)

        self.remove = False
        self.invulnerable = False
        self.can_pre_update = False

    def pre_update(self, data):
        pass
    
    @abstractmethod
    def update(self, data):
        pass

    @abstractmethod
    def tick(self, data):
        pass

    @abstractmethod
    def render(self, camera):
        pass

    def __str__(self):
        return f"{self.type} at ({round(self.x, 2)}, {round(self.y, 2)})"

    def get_distance(self, dx, dy):
        return (dx ** 2 + dy ** 2) ** 0.5
    
    def get_velocity(self, dx, dy, speed):
        return (dx / self.get_distance(dx, dy) * speed if dx != 0 or dy != 0 else 0, dy / self.get_distance(dx, dy) * speed if dx != 0 or dy != 0 else 0)
    
    def get_collision(self, other):
        _distance = self.get_distance(self.x - other.x, self.y - other.y)
        return _distance <= self.width / 2 + other.width / 2 or _distance <= self.height / 2 + other.height / 2
    
    def get_room_collision_x(self, room):
            return (self.x + self.width / 2 > room.width / 2 or self.x - self.width / 2 < -room.width / 2)
    
    def get_room_collision_y(self, room):
            return (self.y + self.height / 2 > room.height / 2 or self.y - self.height / 2 < -room.height / 2)

    def get_object_collision(self, object_list):
        for object in object_list:
            if (self.x - self.width / 2 < object.x + object.width / 2) and \
            (self.x + self.width / 2 > object.x - object.width / 2) and \
            (self.y  - self.width / 2 < object.y + object.height / 2) and \
            (self.y + self.height / 2 > object.y - object.height / 2):
                return True
            
        return 
    # TODO this causes movement on all axes to become limited. find a fix.

    def get_out_of_view(self, camera):
        return self.x - self.width / 2 - camera.x + camera.shake_x > camera.width or \
        self.x + self.width / 2 - camera.x + camera.shake_x < 0 or \
        self.y - self.height / 2 - camera.y + camera.shake_y > camera.height or \
        self.y + self.height / 2 - camera.y + camera.shake_y < 0
    
    def get_instance_in_range(self, other, range):
        return self.get_distance((other.x + other.width / 2) - (self.x + self.width / 2), (other.y + other.height / 2) - (self.y + self.height / 2)) <= range
    
    def set_sprite(self, file):
        self.spritepath = file
        self._sprite = pygame.image.load(os.path.join(BASE_DIR, *file.replace("\\", "/").split("/"))).convert_alpha()
        self._sprite = pygame.transform.scale(self._sprite, (round(self.width), round(self.height)))
    """
    def tint_surface(surface, color):
        tinted = surface.copy()
        tinted.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        return tinted
    """