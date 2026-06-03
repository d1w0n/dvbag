from scripts.instance import Instance
import pygame
import math
import random

pygame.init()

class Player(Instance):

    def __init__(self, window, x, y, width, height, health: int, speed: int):
        super().__init__("Player", "assets/images/placeholder.png", window, x, y, width, height)
        self.health = health
        self.speed = speed

        self._dx = 0
        self._dy = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self._color = (0, 0, 255)
        self.projectile_ticks = 0
        self.projectile_cooldown = 100
        self._damage_cooldown = 1000
        self._damage_ticks = 0
        self._mouse_dx = 0
        self._mouse_dy = 0
        self.beam_ticks = 0
        self.beam_cooldown = 50
        self.parry_ticks = 0
        self.parry_cooldown = 1000
    
    def update(self, data): 
        for instance in data["instances"].all_instances:
            if instance.type == "Enemy" or instance.type == "EnemyProjectile" or instance.type == "ChargerEnemy":
                if self.get_collision(instance) and (pygame.time.get_ticks() - self._damage_ticks) > self._damage_cooldown:
                    self._damage_ticks = pygame.time.get_ticks()
                    self.health -= instance.damage
                    data["camera"].shake(100, 100)
                    data["camera"].add_effect("assets/images/red.png", 1000, 100)

            elif instance.type == "EnemyParticle":
                if self.get_collision(instance):
                    self.health += 5
                    if self.health > 100:
                        self.health = 100
        
        key = pygame.key.get_pressed()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self._mouse_dx = mouse_x - (self.x - data["camera"].x)
        self._mouse_dy = mouse_y - (self.y - data["camera"].y)

        self._dx = 0
        self._dy = 0
        # reset target x and y.

        if key[pygame.K_LSHIFT]:
            self.speed = 10
        else:
            self.speed = 5
        # sprinting mechanic.

        if key[pygame.K_w]:
            self._dy = -self.speed
        if key[pygame.K_a]:
            self._dx = -self.speed
        if key[pygame.K_s]:
            self._dy = self.speed
        if key[pygame.K_d]:
            self._dx = self.speed
        # player movement.

        if self.health <= 0:
            self.remove = True

    def tick(self, data):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.velocity_x, self.velocity_y = self.get_velocity(self._dx, self._dy, self.speed)
        self.x += self.velocity_x
        self.y += self.velocity_y
        # adds x and y by velocities.

        if self.get_room_collision_x(data["room"]):
            self.x -= self.velocity_x
        if self.get_room_collision_y(data["room"]):
            self.y -= self.velocity_y
        # if colliding with room bounds, revert x or y velocity change.

        self._angle = -math.degrees(math.atan2(self._mouse_dy, self._mouse_dx))
        # determine sprite rotation angle.

        if pygame.mouse.get_pressed()[0] and (pygame.time.get_ticks() - self.projectile_ticks) > self.projectile_cooldown:
            self.projectile_ticks = pygame.time.get_ticks()
            data["instances"].add_Projectile(self._window, self.x, self.y, 24, 24, mouse_x + data["camera"].x, mouse_y + data["camera"].y, 24, 25)
            for i in range(3):
                data["instances"].add_ProjectileParticle(self._window, self.x, self.y, 12, 12, "assets/images/dot.png", 15, math.degrees(math.atan2(mouse_y + data["camera"].y - self.y, mouse_x + data["camera"].x - self.x)) + random.randint(-45, 45), 250)
            data["camera"].shake(7, 7)
        # if mouse is down, create a projectile instance at player position going towards mouse position, then shake the camera by 5.
        
        if pygame.mouse.get_pressed()[2] and (pygame.time.get_ticks() - self.beam_ticks) > self.beam_cooldown:
            self.beam_ticks = pygame.time.get_ticks()
            data["instances"].add_Beam(self._window, self.x, self.y, 24, 24, mouse_x + data["camera"].x, mouse_y + data["camera"].y, 15)
            for i in range(3):
                data["instances"].add_ProjectileParticle(self._window, self.x, self.y, 12, 12, "assets/images/magentadot.png", 20, math.degrees(math.atan2(mouse_y + data["camera"].y - self.y, mouse_x + data["camera"].x - self.x)) + random.randint(-45, 45), 150)
            data["camera"].shake(5, 5)
        # creates a beam instead.

        if pygame.key.get_pressed()[pygame.K_f] and (pygame.time.get_ticks() - self.parry_ticks) > self.parry_cooldown:
            self.parry_ticks = pygame.time.get_ticks()
            data["instances"].add_Parry(self._window, self.x, self.y, 96, 96, "Player", 10)
            data["camera"].shake(10, 10)
        # if f is down, create a parry instance that reflects enemy projectiles and indicated attacks.

        mouse_x, mouse_y = pygame.mouse.get_pos()
        data["camera"].target(self.x - data["width"] / 2 + (mouse_x - data["width"] / 2) / 4, self.y - data["height"] / 2 + (mouse_y - data["height"] / 2) / 4)
        # smooths camera position to mouse and player position.

        for element in data["ui"].ui_list:
                if element.name == "HealthBar":
                    element.stat = self.health

                if element.name == "HealthText":
                    element.set_text("Health: " + str(self.health) + "")
        # updates ui elements correlated to player stats.
        
    def render(self, camera):
        _rotated = pygame.transform.rotate(self._sprite, self._angle)
        _rect = _rotated.get_rect(center=(self.x - camera.x + camera.shake_x, self.y - camera.y + camera.shake_y))
        self._window.blit(_rotated, _rect.topleft)