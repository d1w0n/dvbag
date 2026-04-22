from scripts.instance import Instance
import pygame
import math

pygame.init()

class Player(Instance):

    def __init__(self, window, x, y, width, height, health: int, speed: int):
        super().__init__("Player", "assets/placeholder.png", window, x, y, width, height)
        self.health = health
        self.speed = speed

        self._dx = 0
        self._dy = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self._color = (0, 0, 255)
        self.cooldown_ticks = 0
        self.projectile_cooldown = 100
        self._damage_cooldown = 1000
        self._damage_ticks = 0
        self._mouse_dx = 0
        self._mouse_dy = 0
    
    def update(self, instance_list, room, camera): 
        self._room_width = room.width
        self._room_height = room.height
        
        for instance in instance_list:
            if instance.type == "Enemy":
                if self.get_collision(instance) and (pygame.time.get_ticks() - self._damage_ticks) > self._damage_cooldown:
                    self._damage_ticks = pygame.time.get_ticks()
                    self.health -= instance.damage
                    camera.shake(50, 50) 
        
        key = pygame.key.get_pressed()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self._mouse_dx = mouse_x - (self.x - camera.x)
        self._mouse_dy = mouse_y - (self.y - camera.y)

        self._dx = 0
        self._dy = 0
        # reset target x and y.

        if key[pygame.K_LSHIFT]:
            self.speed = 10
        else:
            self.speed = 5
        if key[pygame.K_w]:
            self._dy = -self.speed
        if key[pygame.K_a]:
            self._dx = -self.speed
        if key[pygame.K_s]:
            self._dy = self.speed
        if key[pygame.K_d]:
            self._dx = self.speed
        # player movement.

    def tick(self):
        self._target_distance = (self._dx ** 2 + self._dy ** 2) ** 0.5 
        # use pythagorean theorem to stop extra diagonal speed.

        if self._target_distance > 0:
            self.x_velocity = self._dx / self._target_distance * self.speed
            self.y_velocity = self._dy / self._target_distance * self.speed
        # sets velocity to move towards the target.

        else:
            self.x_velocity = 0
            self.y_velocity = 0
        # if no movement, set velocity to 0.

        self.x += self.x_velocity
        self.y += self.y_velocity
        # adds x and y by velocities.

        if self.get_room_collision_x():
            self.x -= self.x_velocity
        if self.get_room_collision_y():
            self.y -= self.y_velocity
        # if colliding with room bounds, revert x or y velocity change.

        self._angle = -math.degrees(math.atan2(self._mouse_dy, self._mouse_dx))
        
    def render(self, camera_x, camera_y):
        _rotated = pygame.transform.rotate(self._sprite, self._angle)
        _rect = _rotated.get_rect(center=(self.x - camera_x, self.y - camera_y))
        self._window.blit(_rotated, _rect.topleft)