from scripts.instance import Instance
import pygame
import math

pygame.init()

class Enemy(Instance):

    def __init__(self, window, x, y, width, height, health: int, speed: int, damage: int):
        super().__init__("Enemy", "assets/placeholder_red.png", window, x, y, width, height)
        self.health = health
        self.speed = speed
        self.damage = damage

        self.x_target = 0
        self.y_target = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self._alpha = 255
        self._alpha_offset = 0

    def update(self, instance_list, room, camera):
        self._alpha_offset *= 0.8

        for instance in instance_list:
            if instance.type == "Player":
                self.x_target = instance.x
                self.y_target = instance.y
                # sets target position to go to the player.
            
            if instance.type == "Projectile":
                if self.get_collision(instance):
                    self.health -= instance.damage
                    self._alpha_offset = 255
                # checks for collision with projectiles. if collision is true, subtract health by the projectile damage.

        if self.health <= 0:
            self.remove = True
                
    def tick(self):
        self._dx = self.x_target - self.x
        self._dy = self.y_target - self.y
        self.velocity_x = self.get_velocity_x(self._dx, self._dy, self.speed)
        self.velocity_y = self.get_velocity_y(self._dx, self._dy, self.speed)
        self.x += self.velocity_x
        self.y += self.velocity_y
        # moves towards the target position.

        self._angle = -math.degrees(math.atan2(self._dy, self._dx))

    def render(self, camera_x, camera_y):
        _rotated = pygame.transform.rotate(self._sprite, self._angle)
        _rotated.set_alpha(self._alpha - self._alpha_offset)
        _rect = _rotated.get_rect(center=(self.x - camera_x, self.y - camera_y))
        self._window.blit(_rotated, _rect.topleft)



class ProjectileEnemy(Enemy):
    def __init__(self, window, x, y, width, height, health: int, speed: int, damage: int, range, cooldown = 1000):
        super().__init__(window, x, y, width, height, health, speed, damage)
        self.range = range

        self.type = "ProjectileEnemy"
        self.spawn_projectile = False
        self.cooldown_ticks = 0
        self.projectile_cooldown = cooldown
    
    def update(self, instance_list, room, camera):
        self._alpha_offset *= 0.8

        for instance in instance_list:
            if instance.type == "Player":
                self.x_target = instance.x
                self.y_target = instance.y
                # sets target position to go to the player.

                if self.get_instance_in_range(instance, self.range):
                    self.spawn_projectile = True
                else:
                    self.spawn_projectile = False
            
            if instance.type == "Projectile":
                if self.get_collision(instance):
                    self.health -= instance.damage
                    self._alpha_offset = 255
                # checks for collision with projectiles. if collision is true, subtract health by the projectile damage.

        if self.health <= 0:
            self.remove = True