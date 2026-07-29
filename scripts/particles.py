import pygame
import math
from scripts.instance import Instance

pygame.init()

class Particle(Instance):
    def __init__(self, window, sprite, x, y, width, height, direction, speed, drag, duration):
        super().__init__("Particle", sprite, window, x, y, width, height)
        self.speed = speed
        self.direction = direction
        self.drag = drag
        self.duration = duration

        self._init_ticks = pygame.time.get_ticks()
        self._alpha = 255
        self.supertype = "Particle"

    def update(self, data):
        if (pygame.time.get_ticks() - self._init_ticks) > self.duration:
            self.remove = True

    def tick(self, data):
        self.velocity_x = self.speed * math.cos(math.radians(self.direction))
        self.velocity_y = self.speed * math.sin(math.radians(self.direction))
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.speed *= self.drag

        if self.get_room_collision_x(data["room"]):
            self.x -= self.velocity_x
        if self.get_room_collision_y(data["room"]):
            self.y -= self.velocity_y

    def render(self, camera):
        self._sprite.set_alpha(255 - round(255 * ((pygame.time.get_ticks() - self._init_ticks) / self.duration)))
        self._window.blit(self._sprite, (self.x - self.width / 2 - camera.x + camera.shake_x, self.y - self.height / 2 - camera.y + camera.shake_y))

class EnemyParticle(Particle):
    def __init__(self, window, x, y, width, height, direction, speed, drag, duration):
        super().__init__(window, "assets/images/placeholder_green.png", x, y, width, height, direction, speed, drag, duration)
        self.type = "EnemyParticle"

    def update(self, data):
        for instance in data["instances"].all_instances:
            if instance.type == "Player":
                if self.get_collision(instance):
                    self.remove = True

        super().update(data)

class ProjectileParticle(Particle):
    def __init__(self, window, sprite, x, y, width, height, direction, speed, drag, duration):
        super().__init__(window, sprite, x, y, width, height, direction, speed, drag, duration)
        self.type = "ProjectileParticle"

    def update(self, data):
        if self.get_room_collision_x(data["room"]) or self.get_room_collision_y(data["room"]):
            self.remove = True

        super().update(data)

class ParryFlash(Particle):
    def __init__(self, window, x, y, width, height, direction, duration, rotation_speed = 0):
        super().__init__(window, "assets/images/parryflash.png", x, y, width, height, direction, 0, 0, duration)
        self._rotation_speed = rotation_speed

    def tick(self, data):
        self.direction += self._rotation_speed
        self.height += 5
        self.set_sprite(self.spritepath)

    def render(self, camera):
        _rotated = pygame.transform.rotate(self._sprite, self.direction)
        _rotated.set_alpha(255 - round(255 * ((pygame.time.get_ticks() - self._init_ticks) / self.duration)))
        _rect = _rotated.get_rect(center=(self.x - camera.x + camera.shake_x, self.y - camera.y + camera.shake_y))
        self._window.blit(_rotated, _rect.topleft)

class AfterImage(Particle):
    def __init__(self, window, sprite, x, y, width, height, direction, duration, strength, size_change = 0):
        super().__init__(window, sprite, x, y, width, height, direction, 0, 0, duration)
        self.strength = strength
        self.size_change = size_change

    def update(self, data):
        if self.width <= 0 or self.height <= 0:
            self.remove = True

        super().update(data)

    def tick(self, data):
        self.width += self.size_change
        self.height += self.size_change
        self.set_sprite(self.spritepath)

    def render(self, camera):
        if not self.remove:
            _rotated = pygame.transform.rotate(self._sprite, self.direction)
            _rotated.set_alpha(self.strength - round(self.strength * ((pygame.time.get_ticks() - self._init_ticks) / self.duration)))
            _rect = _rotated.get_rect(center=(self.x - camera.x + camera.shake_x, self.y - camera.y + camera.shake_y))
            self._window.blit(_rotated, _rect.topleft)

class TextDisplay(Particle):
    def __init__(self, window, x, y, text = "", size = 12, color = (0, 0, 0), font = None, direction = 0, speed = 0, drag = 0, duration = 1000):
        super().__init__(window, None, x, y, 0, 0, direction, speed, drag, duration)
        self.color = color
        self.font = pygame.font.Font(font, size)
        self.set_text(text)
    
    def render(self, camera):
        self._sprite.set_alpha(255 - round(255 * ((pygame.time.get_ticks() - self._init_ticks) / self.duration)))
        self._window.blit(self._text_surface, (self.x - camera.x + camera.shake_x, self.y - camera.y + camera.shake_y))

    def set_text(self, text):
        self._text_surface = self.font.render(text, True, self.color)

class BeamFade(Particle):
    def __init__(self, window, x_init, y_init, x, y, width, height, duration):
        super().__init__(window, None, x, y, width, height, 0, 0, 0, duration)
        self.type = "BeamFade"
        self._x_init = x_init
        self._y_init = y_init
        self._width_init = width
        self.always_render = True

    def tick(self, data):
        self.width = self._width_init - self._width_init * ((pygame.time.get_ticks() - self._init_ticks) / self.duration)

    def render(self, camera):
        pygame.draw.line(self._window, (255, 0, 255), (self._x_init - camera.x + camera.shake_x, self._y_init - camera.y + camera.shake_y), (self.x - camera.x + camera.shake_x, self.y - camera.y + camera.shake_y), round(self.width))
        pygame.draw.circle(self._window, (255, 0, 255), (self.x - camera.x + camera.shake_x, self.y - camera.y + camera.shake_y), round(self.width / 2))

class ExplosionFade(Particle):
    def __init__(self, window, x, y, radius, duration):
        super().__init__(window, "assets/images/placeholder_red.png", x, y, radius, radius, 0, 0, 0, duration)
        self.type = "ExplosionFade"
        self.radius = radius
        self._init_radius = radius
        self.duration = duration

        self._init_ticks = pygame.time.get_ticks()
        self._new_size = radius

    def update(self, data):
        if (pygame.time.get_ticks() - self._init_ticks) > self.duration:
            self.remove = True

        self._new_size += self._init_radius * 0.05

    def tick(self, data):
        self.radius = self._new_size
        self.width = self.radius
        self.height = self.radius
        self.set_sprite(self.spritepath)

    def render(self, camera):
        self._sprite.set_alpha(255 - round(255 * ((pygame.time.get_ticks() - self._init_ticks) / self.duration)))
        self._window.blit(self._sprite, (self.x - self.width / 2 - camera.x + camera.shake_x, self.y - self.height / 2 - camera.y + camera.shake_y))