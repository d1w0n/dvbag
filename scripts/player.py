from scripts.instance import Instance
import pygame
import math
import random
import config

pygame.init()

class Player(Instance):

    def __init__(self, window, sprite, x, y, width, height, health, speed):
        super().__init__("Player", "Player", sprite, window, x, y, width, height)
        self.health = health
        self.default_speed = speed
        self.speed = speed

        self.velocity_x = 0
        self.velocity_y = 0
        self.weapon = "Projectile"
        self.primary_ticks = 0
        self.primary_cooldown = 100
        self.damage_cooldown = 1000
        self.damage_ticks = 0
        self.secondary_ticks = 0
        self.secondary_cooldown = 50
        self.parry_ticks = 0
        self.parry_cooldown = 500
        self.dashing = False
        self.dash_ticks = 0
        self.dash_cooldown = 500
        self.dash_duration = 250
        self._angle = 0

    def update_health_ui(self, ui_list):
        for element in ui_list:
            if element.name == "HealthBar":
                element.stat = self.health

            if element.name == "HealthText":
                element.set_text("Health: " + str(self.health) + "")

    def recieve_damage(self, damage, data):
        self.damage_ticks = pygame.time.get_ticks()
        self.health -= damage

        data["camera"].add_shake(100)
        data["ui"].add_ScreenEffect("DamageEffect", self._window, "assets/images/red.png", data["width"], data["height"], 1000, 100)

        self.update_health_ui(data["ui"].ui_list)
        
    def update(self, data): 
        self.nearby = data["instances"].get_nearby(self.x, self.y)
        if not self.invulnerable and (pygame.time.get_ticks() - self.damage_ticks) > self.damage_cooldown:
            for enemy in self.nearby["Enemy"]:
                if enemy.type not in ("Enemy", "ChargerEnemy"):
                    continue

                if self.get_collision(enemy):
                    self.recieve_damage(enemy.damage, data)

            for projectile in self.nearby["Projectile"]:
                if not projectile.type == "EnemyProjectile":
                    continue
                
                if self.get_collision(projectile):
                    self.recieve_damage(projectile.damage, data)

        if self.health < 100:
            for particle in self.nearby["Particle"]:
                if not particle.type == "EnemyParticle":
                    continue
            
                self.health += 5
                if self.health > 100: self.health = 100
                self.update_health_ui(data["ui"].ui_list)
                    
        key = pygame.key.get_pressed()
        
        if key[pygame.K_LSHIFT] and not self.dashing and (pygame.time.get_ticks() - self.dash_ticks) > self.dash_cooldown:
            self.dash_ticks = pygame.time.get_ticks()
            self.dashing = True
            self.invulnerable = True
            self.speed = self.default_speed * 2

        if self.dashing and (pygame.time.get_ticks() - self.dash_ticks) > self.dash_duration:
            self.dash_ticks = pygame.time.get_ticks()
            self.dashing = False
            self.invulnerable = False
            self.speed = self.default_speed

        if key[pygame.K_1]:
            self.weapon = "Projectile"
            self.primary_cooldown = 100
            self.secondary_cooldown = 50
            for element in data["ui"].ui_list:
                if element.name == "WeaponText":
                    element.set_text("weapon: " + self.weapon)

        elif key[pygame.K_2]:
            self.weapon = "Shotgun"
            self.primary_cooldown = 200
            self.secondary_cooldown = 1000
            for element in data["ui"].ui_list:
                if element.name == "WeaponText":
                    element.set_text("weapon: " + self.weapon)

        elif key[pygame.K_3]:
            self.weapon = "Melee"
            self.primary_cooldown = 200
            self.secondary_cooldown = 500
            for element in data["ui"].ui_list:
                if element.name == "WeaponText":
                    element.set_text("weapon: " + self.weapon)

        self._dx = 0
        self._dy = 0

        if key[pygame.K_w]:
            self._dy = -self.speed
        if key[pygame.K_a]:
            self._dx = -self.speed
        if key[pygame.K_s]:
            self._dy = self.speed
        if key[pygame.K_d]:
            self._dx = self.speed
        # player movement.

        if self.health <= 0 and not config.IMMORTAL:
            self.remove = True

    def tick(self, data):
        self.velocity_x, self.velocity_y = self.get_velocity(self._dx, self._dy, self.speed)
        self.x += self.velocity_x
        self.y += self.velocity_y
        # adds x and y by velocities.

        if self.get_room_collision_x(data["room"]):
            self.x -= self.velocity_x
        if self.get_room_collision_y(data["room"]):
            self.y -= self.velocity_y
        if self.get_object_collision(data["objects"].object_list):
            self.x -= self.velocity_x
            self.y -= self.velocity_y
        # if colliding with room bounds, revert x or y velocity change.

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self._mouse_dx = mouse_x - (self.x - data["camera"].x)
        self._mouse_dy = mouse_y - (self.y - data["camera"].y)
        self._angle = -math.degrees(math.atan2(self._mouse_dy, self._mouse_dx))
        # determine sprite rotation angle.

        if not self.invulnerable:
            if pygame.key.get_pressed()[pygame.K_f] and (pygame.time.get_ticks() - self.parry_ticks) > self.parry_cooldown:
                self.parry_ticks = pygame.time.get_ticks()
                data["instances"].add_Parry(self._window, self.x, self.y, 96, 96, "Player", 200, 10)
                data["camera"].add_shake(10)
            # if f is down, create a parry instance that reflects enemy projectiles and indicated attacks.

            if self.weapon == "Projectile":
                if pygame.mouse.get_pressed()[0] and (pygame.time.get_ticks() - self.primary_ticks) > self.primary_cooldown:
                    self.primary_ticks = pygame.time.get_ticks()
                    data["instances"].add_Projectile(self._window, "assets/images/placeholder.png", self.x, self.y, 24, 24, math.degrees(math.atan2(mouse_y + data["camera"].y - self.y, mouse_x + data["camera"].x - self.x)), 24, 1, 25)
                    for i in range(3):
                        data["instances"].add_ProjectileParticle(self._window, "assets/images/dot.png", self.x, self.y, 12, 12, math.degrees(math.atan2(mouse_y + data["camera"].y - self.y, mouse_x + data["camera"].x - self.x)) + random.randint(-45, 45), 15, 1, 250)
                    data["camera"].add_shake(7)
                # if mouse is down, create a projectile instance at player position going towards mouse position, then shake the camera by 5.
                
                if pygame.mouse.get_pressed()[2] and (pygame.time.get_ticks() - self.secondary_ticks) > self.secondary_cooldown:
                    self.secondary_ticks = pygame.time.get_ticks()
                    data["instances"].add_Beam(self._window, self.x, self.y, 24, 24, math.degrees(math.atan2(mouse_y + data["camera"].y - self.y, mouse_x + data["camera"].x - self.x)), 15)
                    for i in range(3):
                        data["instances"].add_ProjectileParticle(self._window, "assets/images/magentadot.png", self.x, self.y, 12, 12, math.degrees(math.atan2(mouse_y + data["camera"].y - self.y, mouse_x + data["camera"].x - self.x)) + random.randint(-45, 45), 20, 1, 150)
                    data["camera"].add_shake(5)
                # creates a beam instead.

            elif self.weapon == "Shotgun":
                if pygame.mouse.get_pressed()[0] and (pygame.time.get_ticks() - self.primary_ticks) > self.primary_cooldown:
                    self.primary_ticks = pygame.time.get_ticks()
                    for i in range(5):
                        data["instances"].add_Beam(self._window, self.x, self.y, 24, 24, math.degrees(math.atan2(mouse_y + data["camera"].y - self.y, mouse_x + data["camera"].x - self.x)) + random.randint(-30, 30), 15)
                    for i in range(3):
                        data["instances"].add_ProjectileParticle(self._window, "assets/images/magentadot.png", self.x, self.y, 12, 12, math.degrees(math.atan2(mouse_y + data["camera"].y - self.y, mouse_x + data["camera"].x - self.x)) + random.randint(-45, 45), 20, 1, 150)
                    data["camera"].add_shake(5)
                
                if pygame.mouse.get_pressed()[2] and (pygame.time.get_ticks() - self.secondary_ticks) > self.secondary_cooldown:
                    self.secondary_ticks = pygame.time.get_ticks()
                    data["instances"].add_BombProjectile(self._window, "assets/images/placeholder.png", self.x, self.y, 24, 24, math.degrees(math.atan2(mouse_y + data["camera"].y - self.y, mouse_x + data["camera"].x - self.x)), 10, 0.9, 1000, 192, 100)
                    data["camera"].add_shake(25)

            elif self.weapon == "Melee":
                if pygame.mouse.get_pressed()[0] and (pygame.time.get_ticks() - self.primary_ticks) > self.primary_cooldown:
                    self.primary_ticks = pygame.time.get_ticks()
                    data["instances"].add_Melee(self._window, self.x, self.y, 144, 144, "Player", 100, 50)

        data["camera"].target(self.x - data["width"] / 2 + (mouse_x - data["width"] / 2) / 4, self.y - data["height"] / 2 + (mouse_y - data["height"] / 2) / 4)
        # smooths camera position to mouse and player position.

        if self.dashing:
            data["instances"].add_AfterImage(self._window, self.spritepath, self.x, self.y, self.width, self.height, self._angle, 250, 125, -1)
        
    def render(self, camera):
        _rotated = pygame.transform.rotate(self._sprite, self._angle)
        _rect = _rotated.get_rect(center=(self.x - camera.x + camera.shake_x, self.y - camera.y + camera.shake_y))
        self._window.blit(_rotated, _rect.topleft)