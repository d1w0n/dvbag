from scripts.instance import Instance
import pygame
import math
import random

pygame.init()

class Enemy(Instance):

    def __init__(self, window, sprite, x, y, width, height, health, speed, damage):
        super().__init__("Enemy", sprite, window, x, y, width, height)
        self.health = health
        self.speed = speed
        self.damage = damage

        self.target_instance = "Player"
        self.target_x = 0
        self.target_y = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self._alpha = 255
        self._alpha_offset = 0
        self.phase = 1
        self._angle = 0
        
        self.phase_info = {
            0: "Idle",
            1: "Roaming"
        }

    def update(self, data):
        self._alpha_offset *= 0.8

        for instance in data["instances"].all_instances:
            if instance.type == self.target_instance:
                self.target_x = instance.x
                self.target_y = instance.y
                # sets target position to go to the player.
            
            elif instance.type == "Projectile" or instance.type == "Beam":
                if self.get_collision(instance):
                    self.health -= instance.damage
                    self._alpha_offset = 255

                    data["score"] += 5
                    data["ui"].add_TextParticle("ScoreParticle", self._window, random.randint(10, 150), data["height"] - 50, 24, "+5", (0, 0, 0), None, 1000, random.randint(-1, 1), random.randint(-10, -5))
                    for element in data["ui"].ui_list:
                        if element.name == "ScoreText":
                            element.set_text("Score: " + str(data["score"]))
                # checks for collision with projectiles. if collision is true, subtract health by the projectile damage.

        if self.health <= 0:
            self.remove = True

            data["score"] += 50
            data["ui"].add_TextParticle("ScoreParticle", self._window, random.randint(10, 150), data["height"] - 50, 24, "+50", (0, 0, 0), None, 1000, random.randint(-1, 1), random.randint(-10, -5))
            for element in data["ui"].ui_list:
                if element.name == "ScoreText":
                    element.set_text("Score: " + str(data["score"]))
                
    def tick(self, data):
        self._dx = self.target_x - self.x
        self._dy = self.target_y - self.y

        self.velocity_x, self.velocity_y = self.get_velocity(self._dx, self._dy, self.speed)
        if not self.phase == 0:
            self.x += self.velocity_x
            self.y += self.velocity_y

            self._angle = -math.degrees(math.atan2(self._dy, self._dx))
        # moves towards the target position and angle.

        if self.remove:
            for i in range(5):
                data["instances"].add_EnemyParticle(self._window, self.x, self.y, 24, 24, random.randint(1, 360), random.randint(5, 10), 0.9, 3000)
            # create 5 particles on death. 

    def render(self, camera):
        _rotated = pygame.transform.rotate(self._sprite, self._angle)
        _rotated.set_alpha(self._alpha - self._alpha_offset)
        _rect = _rotated.get_rect(center=(self.x - camera.x + camera.shake_x, self.y - camera.y + camera.shake_y))
        self._window.blit(_rotated, _rect.topleft)

class ProjectileEnemy(Enemy):
    def __init__(self, window, x, y, width, height, health, speed, damage, range, cooldown = 1000):
        super().__init__(window, "assets/images/placeholder_dark_red.png", x, y, width, height, health, speed, damage)
        self.range = range

        self.type = "ProjectileEnemy"
        self.spawn_projectile = False
        self.cooldown_ticks = 0
        self.projectile_cooldown = cooldown

        self.phase_info = {
            0: "Idle",
            1: "Roaming",
            2: "Preparing",
            3: "Cooldown"
        }
    
    def update(self, data): 
        self._alpha_offset *= 0.8

        for instance in data["instances"].all_instances:
            if instance.type == "Player":
                self.target_x = instance.x
                self.target_y = instance.y
                # sets target position to go to the player.

                if self.get_instance_in_range(instance, self.range):
                    self.spawn_projectile = True
                else:
                    self.spawn_projectile = False
            
            elif instance.type == "Projectile" or instance.type == "Beam" or instance.type == "Explosion":
                if self.get_collision(instance):
                    self.health -= instance.damage
                    self._alpha_offset = 255

                    data["score"] += 5
                    data["ui"].add_TextParticle("ScoreParticle", self._window, random.randint(10, 150), data["height"] - 50, 24, "+5", (0, 0, 0), None, 1000, random.randint(-1, 1), random.randint(-10, -5))
                    for element in data["ui"].ui_list:
                        if element.name == "ScoreText":
                            element.set_text("Score: " + str(data["score"]))
                # checks for collision with projectiles. if collision is true, subtract health by the projectile damage.

        if self.health <= 0:
            self.remove = True

            data["score"] += 50
            data["ui"].add_TextParticle("ScoreParticle", self._window, random.randint(10, 150), data["height"] - 50, 24, "+50", (0, 0, 0), None, 1000, random.randint(-1, 1), random.randint(-10, -5))
            for element in data["ui"].ui_list:
                if element.name == "ScoreText":
                    element.set_text("Score: " + str(data["score"]))

    def tick(self, data):
        self._dx = self.target_x - self.x
        self._dy = self.target_y - self.y

        if not self.spawn_projectile:
            self.velocity_x, self.velocity_y = self.get_velocity(self._dx, self._dy, self.speed)
            if not self.phase == 0:
                self.x += self.velocity_x
                self.y += self.velocity_y

        if not self.phase == 0:
            self._angle = -math.degrees(math.atan2(self._dy, self._dx))
        # moves towards the target position and angle.

        if self.spawn_projectile and (pygame.time.get_ticks() - self.cooldown_ticks) > self.projectile_cooldown:
                self.cooldown_ticks = pygame.time.get_ticks()
                data["instances"].add_EnemyProjectile(self._window, self.x, self.y, 24, 24, math.degrees(math.atan2(self._dy, self._dx)), 10, 1, 10)
                for i in range(3):
                    data["instances"].add_ProjectileParticle(self._window, "assets/images/enemyprojectile.png", self.x, self.y, 12, 12, math.degrees(math.atan2(self.target_y - self.y, self.target_x - self.x)) + random.randint(-45, 45), 15, 1, 250)
            # if player is in range, fire a projectile at the player.

        if self.remove:
            for i in range(5):
                data["instances"].add_EnemyParticle(self._window, self.x, self.y, 24, 24, random.randint(1, 360), random.randint(5, 10), 0.9, 3000)
            # create 5 particles on death. 

class ChargerEnemy(Enemy):
    def __init__(self, window, x, y, width, height, health, speed, damage, range):
        super().__init__(window, "assets/images/placeholder_red.png", x, y, width, height, health, speed, damage)
        self.range = range

        self.type = "ChargerEnemy"
        self._phase_ticks = pygame.time.get_ticks()
        self.spawn_particle = False

        self.phase_info = {
            0: "Idle",
            1: "Roaming",
            2: "Preparing",
            3: "Charging",
            4: "Recovering"
        }

    def update(self, data):
        self._alpha_offset *= 0.8
        for instance in data["instances"].all_instances:
            if instance.type == "Player":
                self.target_x = instance.x
                self.target_y = instance.y

                if self.phase == 1 and self.get_instance_in_range(instance, self.range):
                    self.phase = 2
                    self._phase_ticks = pygame.time.get_ticks()
                    self.spawn_particle = True

                elif self.phase == 3 and self.get_collision(instance):
                    self.phase = 4
                    self._phase_ticks = pygame.time.get_ticks()

            elif instance.type == "Parry" and self.phase == 3:
                if self.get_collision(instance):
                    self.health = 0
                    self.phase = 4
                    self._phase_ticks = pygame.time.get_ticks()

                    data["instances"].add_TextDisplay(self._window, instance.x, instance.y, "+PARRY!", 24, (0, 0, 0), None, random.randint(60, 120), 5, 0.9, 1000)
                    data["instances"].add_Particle(self._window, "assets/images/placeholder.png", instance.x, instance.y, 12, 12, random.randint(0, 360), random.randint(5, 10), 0.9, 250)
                    data["score"] += 25
                    data["ui"].add_TextParticle("ScoreParticle", self._window, random.randint(10, 150), data["height"] - 50, 24, "+25", (0, 0, 0), None, 1000, random.randint(-1, 1), random.randint(-10, -5))
                    for element in data["ui"].ui_list:
                        if element.name == "ScoreText":
                            element.set_text("Score: " + str(data["score"]))

            elif instance.type == "Projectile" or instance.type == "Beam" or instance.type == "Explosion":
                if self.get_collision(instance):
                    self.health -= instance.damage
                    self._alpha_offset = 255

                    data["score"] += 5
                    data["ui"].add_TextParticle("ScoreParticle", self._window, random.randint(10, 150), data["height"] - 50, 24, "+5", (0, 0, 0), None, 1000, random.randint(-1, 1), random.randint(-10, -5))
                    for element in data["ui"].ui_list:
                        if element.name == "ScoreText":
                            element.set_text("Score: " + str(data["score"]))
                # checks for collision with projectiles. if collision is true, subtract health by the projectile damage.
        # check for interactions with other instances.

        if self.phase == 2 and (pygame.time.get_ticks() - self._phase_ticks) > 500:
                self.phase = 3
                self._phase_ticks = pygame.time.get_ticks()

        elif self.phase == 3 and (pygame.time.get_ticks() - self._phase_ticks) > 500:
                self.phase = 4
                self._phase_ticks = pygame.time.get_ticks()

        elif self.phase == 4 and (pygame.time.get_ticks() - self._phase_ticks) > 500:
            self.phase = 1

        if self.health <= 0:
            self.remove = True

            data["score"] += 50
            data["ui"].add_TextParticle("ScoreParticle", self._window, random.randint(10, 150), data["height"] - 50, 24, "+50", (0, 0, 0), None, 1000, random.randint(-1, 1), random.randint(-10, -5))
            for element in data["ui"].ui_list:
                if element.name == "ScoreText":
                    element.set_text("Score: " + str(data["score"]))
                    
    def tick(self, data):
        self._dx = self.target_x - self.x
        self._dy = self.target_y - self.y

        if not self.phase == 2 and not self.phase == 4: 
            self.velocity_x, self.velocity_y = self.get_velocity(self._dx, self._dy, self.speed if self.phase == 1 else self.speed * 2)
            self.x += self.velocity_x
            self.y += self.velocity_y
        
        self._angle = -math.degrees(math.atan2(self._dy, self._dx))
        # moves and looks towards the target position.

        if self.phase == 3:
            data["instances"].add_AfterImage(self._window, self.spritepath, self.x, self.y, self.width, self.height, self._angle, 250, 125, -1)

        if self.spawn_particle:
            for i in range(3):
                data["instances"].add_ParryFlash(self._window, self.x, self.y, 12, 48, random.randint(1, 360), 500, random.randint(-10, 10))
            self.spawn_particle = False
            # creates parry indicator particles.

        if self.remove:
            for i in range(5):
                data["instances"].add_EnemyParticle(self._window, self.x, self.y, 24, 24, random.randint(1, 360), random.randint(5, 10), 0.9, 3000)
            # create 5 particles on death. 

class SniperEnemy(Enemy):
    def __init__(self):
        pass