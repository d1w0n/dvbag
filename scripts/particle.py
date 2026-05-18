import pygame
import math
from scripts.instance import Instance

pygame.init()

class Particle(Instance):
    def __init__(self, window, x, y, width, height, speed, direction, duration):
        super().__init__("Particle", "assets/images/placeholder.png", window, x, y, width, height)
        self.speed = speed
        self.direction = direction
        self._speed_decay = 0.9
        self._init_ticks = pygame.time.get_ticks()
        self.duration = duration
        self._alpha = 255
        self.supertype = "Particle"

    def update(self, instance_list, room, camera):
        self._room = room

        if (pygame.time.get_ticks() - self._init_ticks) > self.duration:
            self.remove = True

    def tick(self):
        self.velocity_x = self.speed * math.cos(math.radians(self.direction))
        self.velocity_y = self.speed * math.sin(math.radians(self.direction))
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.speed *= self._speed_decay

        if self.get_room_collision_x(self._room):
            self.x -= self.velocity_x
        if self.get_room_collision_y(self._room):
            self.y -= self.velocity_y

    def render(self, camera_x, camera_y):
        self._sprite.set_alpha(255 - round(255 * ((pygame.time.get_ticks() - self._init_ticks) / self.duration)))
        self._window.blit(self._sprite, (self.x - self.width / 2 - camera_x, self.y - self.height / 2 - camera_y))



class EnemyParticle(Particle):
    def __init__(self, window, x, y, width, height, speed, direction, duration):
        super().__init__(window, x, y, width, height, speed, direction, duration)
        self.type = "EnemyParticle"
        self.set_sprite("assets/images/placeholder_green.png")

    def update(self, instance_list, room, camera):
        for instance in instance_list:
            if instance.type == "Player":
                if self.get_collision(instance):
                    self.remove = True

        super().update(instance_list, room, camera)



class ProjectileParticle(Particle):
    def __init__(self, window, x, y, width, height, sprite, speed, direction, duration):
        super().__init__(window, x, y, width, height, speed, direction, duration)
        self.type = "ProjectileParticle"
        self.set_sprite(sprite)
        self._speed_decay = 1 # constant speed.

    def update(self, instance_list, room, camera):
        self._room = room 
        if self.get_room_collision_x(room) or self.get_room_collision_y(room) or ((pygame.time.get_ticks() - self._init_ticks) > self.duration):
            self.remove = True



class ParryFlash(Particle):
    def __init__(self, window, x, y, width, height, direction, duration, rotation_speed = 0):
        super().__init__(window, x, y, width, height, 0, direction, duration)
        self._rotation_speed = rotation_speed
        self.set_sprite("assets/images/parryflash.png")

    def update(self, instance_list, room, camera):
        super().update(instance_list, room, camera)

    def tick(self):
        self.direction += self._rotation_speed
        self.height += 5
        self.set_sprite("assets/images/parryflash.png")

    def render(self, camera_x, camera_y):
        _rotated = pygame.transform.rotate(self._sprite, self.direction)
        _rotated.set_alpha(255 - round(255 * ((pygame.time.get_ticks() - self._init_ticks) / self.duration)))
        _rect = _rotated.get_rect(center=(self.x - camera_x, self.y - camera_y))
        self._window.blit(_rotated, _rect.topleft)



class AfterImage(Particle):
    def __init__(self, window, sprite, x, y, width, height, direction, duration, strength, size_change = 0):
        super().__init__(window, x, y, width, height, 0, direction, duration)
        self.set_sprite(sprite)
        self.strength = strength
        self._size_change = size_change

    def update(self, instance_list, room, camera):
        if self.width <= 0 or self.height <= 0:
            self.remove = True

        if (pygame.time.get_ticks() - self._init_ticks) > self.duration:
            self.remove = True

    def tick(self):
        self.width += self._size_change
        self.height += self._size_change
        self.set_sprite(self.spritepath)

    def render(self, camera_x, camera_y):
        if not self.remove:
            _rotated = pygame.transform.rotate(self._sprite, self.direction)
            _rotated.set_alpha(self.strength - round(self.strength * ((pygame.time.get_ticks() - self._init_ticks) / self.duration)))
            _rect = _rotated.get_rect(center=(self.x - camera_x, self.y - camera_y))
            self._window.blit(_rotated, _rect.topleft)



class TextDisplay(Particle):
    def __init__(self, window, x, y, speed, direction, duration, size, text = "", color = (0, 0, 0), font = None):
        super().__init__(window, x, y, 0, 0, speed, direction, duration)
        self.color = color
        self.font = pygame.font.Font(font, size)
        self._text_surface = self.font.render(text, True, self.color)
    
    def render(self, camera_x, camera_y):
        self._sprite.set_alpha(255 - round(255 * ((pygame.time.get_ticks() - self._init_ticks) / self.duration)))
        self._window.blit(self._text_surface, (self.x - camera_x, self.y - camera_y))

    def set_text(self, text: str):
        self._text_surface = self.font.render(text, True, self.color)