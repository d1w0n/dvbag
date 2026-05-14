from scripts.instance import Instance
import pygame
import math

pygame.init()

class Enemy(Instance):

    def __init__(self, window, x, y, width, height, health: int, speed: int, damage: int):
        super().__init__("Enemy", "assets/images/placeholder_red.png", window, x, y, width, height)
        self.health = health
        self.speed = speed
        self.damage = damage

        self.target_x = 0
        self.target_y = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self._alpha = 255
        self._alpha_offset = 0
        self.phase = 0
        self.supertype = "Enemy"

    def update(self, instance_list, room, camera):
        self._alpha_offset *= 0.8

        for instance in instance_list:
            if instance.type == "Player":
                self.target_x = instance.x
                self.target_y = instance.y
                # sets target position to go to the player.
            
            elif instance.type == "Projectile" or instance.type == "Beam":
                if self.get_collision(instance):
                    self.health -= instance.damage
                    self._alpha_offset = 255
                    self.add_score += 5
                # checks for collision with projectiles. if collision is true, subtract health by the projectile damage.

        if self.health <= 0:
            self.remove = True
            self.add_score += 50
                
    def tick(self):
        self._dx = self.target_x - self.x
        self._dy = self.target_y - self.y
        self.velocity_x, self.velocity_y = self.get_velocity(self._dx, self._dy, self.speed)
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
        self.set_sprite("assets/images/placeholder_dark_red.png")
    
    def update(self, instance_list, room, camera): 
        self._alpha_offset *= 0.8

        for instance in instance_list:
            if instance.type == "Player":
                self.target_x = instance.x
                self.target_y = instance.y
                # sets target position to go to the player.

                if self.get_instance_in_range(instance, self.range):
                    self.spawn_projectile = True
                else:
                    self.spawn_projectile = False
            
            elif instance.type == "Projectile" or instance.type == "Beam":
                if self.get_collision(instance):
                    self.health -= instance.damage
                    self._alpha_offset = 255
                    self.add_score += 5
                # checks for collision with projectiles. if collision is true, subtract health by the projectile damage.

        if self.health <= 0:
            self.remove = True
            self.add_score += 50

    def tick(self):
        self._dx = self.target_x - self.x
        self._dy = self.target_y - self.y
        if not self.spawn_projectile:
            self.velocity_x, self.velocity_y = self.get_velocity(self._dx, self._dy, self.speed)
            self.x += self.velocity_x
            self.y += self.velocity_y
        # moves towards the target position.

        self._angle = -math.degrees(math.atan2(self._dy, self._dx))



class ChargerEnemy(Enemy):
    def __init__(self, window, x, y, width, height, health, speed, damage, range):
        super().__init__(window, x, y, width, height, health, speed, damage)
        self.range = range
        self.type = "ChargerEnemy"
        self._phase_ticks = pygame.time.get_ticks()
        self.spawn_particle = False

    def update(self, instance_list, room, camera):
        self._alpha_offset *= 0.8
        for instance in instance_list:
            if instance.type == "Player":
                self.target_x = instance.x
                self.target_y = instance.y

                if self.phase == 0 and self.get_instance_in_range(instance, self.range):
                    self.phase = 1
                    self._phase_ticks = pygame.time.get_ticks()
                    self.spawn_particle = True

                elif self.phase == 2 and self.get_collision(instance):
                    self.phase = 3
                    self.trail = False
                    self._phase_ticks = pygame.time.get_ticks()

            elif instance.type == "Parry" and self.phase == 2:
                if self.get_collision(instance):
                    self.phase = 3
                    self.trail = False
                    self._phase_ticks = pygame.time.get_ticks()
                    self.add_score += 25

            elif instance.type == "Projectile" or instance.type == "Beam":
                if self.get_collision(instance):
                    self.health -= instance.damage
                    self._alpha_offset = 255
                    self.add_score += 5
                # checks for collision with projectiles. if collision is true, subtract health by the projectile damage.

        if self.phase == 1 and (pygame.time.get_ticks() - self._phase_ticks) > 500:
                self.phase = 2
                self.trail = True
                self._phase_ticks = pygame.time.get_ticks()

        elif self.phase == 2 and (pygame.time.get_ticks() - self._phase_ticks) > 500:
            self.phase = 3
            self.trail = False
            self._phase_ticks = pygame.time.get_ticks()

        elif self.phase == 3 and (pygame.time.get_ticks() - self._phase_ticks) > 500:
            self.phase = 0

        if self.health <= 0:
            self.remove = True
            self.add_score += 50
                    
    def tick(self):
        self._dx = self.target_x - self.x
        self._dy = self.target_y - self.y
        if not self.phase == 1 and not self.phase == 3: 
            self.velocity_x, self.velocity_y = self.get_velocity(self._dx, self._dy, self.speed if self.phase == 0 else self.speed * 2)
            self.x += self.velocity_x
            self.y += self.velocity_y
        # moves towards the target position.

        self._angle = -math.degrees(math.atan2(self._dy, self._dx))