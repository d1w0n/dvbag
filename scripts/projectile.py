from scripts.instance import Instance
import pygame
import math
import random

pygame.init()

class Projectile(Instance):
    def __init__(self, window, sprite, x, y, width, height, direction, speed, drag, damage, add_x_velocity = 0, add_y_velocity = 0):
        super().__init__("Projectile", sprite, window, x, y, width, height)
        self.direction = direction
        self.speed = speed
        self.drag = drag
        self.damage = damage

        self.parried = False

    def update(self, data):
        for instance in data["instances"].all_instances:
            if instance.type == "Enemy" or instance.type == "ProjectileEnemy" or instance.type == "ChargerEnemy":
                if self.get_collision(instance):
                    self.remove = True
                # if colliding with an enemy, remove itself.

    def tick(self, data):
        self.velocity_x = self.speed * math.cos(math.radians(self.direction))
        self.velocity_y = self.speed * math.sin(math.radians(self.direction))
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.speed *= self.drag
        # change x and y by velocities.

        if self.get_room_collision_x(data["room"]) or self.get_room_collision_y(data["room"]):
            self.remove = True

    def render(self, camera):
        self._window.blit(self._sprite, (self.x - self.width / 2 - camera.x + camera.shake_x, self.y - self.height / 2 - camera.y + camera.shake_y))

class Parry(Projectile):
    def __init__(self, window, x, y, width, height, target_instance, damage):
        super().__init__(window, "assets/images/placeholder.png", x, y, width, height, 0, 0, 0, damage)
        self.type = "Parry"
        self.target_instance = target_instance

        self._init_ticks = pygame.time.get_ticks()
        self.duration = 200
        self._has_target = False
        self.angle_offset = -60

    def update(self, data):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self._has_target = False
        for instance in data["instances"].all_instances:
            if instance.type == self.target_instance:
                self._has_target = True
                self.direction = math.degrees(math.atan2(mouse_y + data["camera"].y - instance.y, mouse_x + data["camera"].x - instance.x)) + self.angle_offset
                self._target_x = (instance.width / 2) * math.cos(math.radians(self.direction)) + instance.x
                self._target_y = (instance.width / 2) * math.sin(math.radians(self.direction)) + instance.y
                
                self.angle_offset = -60 - round(-120 * ((pygame.time.get_ticks() - self._init_ticks) / self.duration))

            elif instance.type == "EnemyProjectile" or (instance.type == "Projectile" and instance.parried) or (instance.type == "ChargerEnemy" and instance.phase == 3):
                if self.get_collision(instance):
                    for instance in data["instances"].all_instances:
                        if instance.type == "Player":
                            instance.parry_ticks = instance.parry_cooldown
                    self.remove = True
        
        if not self._has_target:
            self.remove = True
                
        if (pygame.time.get_ticks() - self._init_ticks) > self.duration:
            self.remove = True

    def tick(self, data):
        self.x = self._target_x
        self.y = self._target_y

    def render(self, camera):
        _rotated = pygame.transform.rotate(self._sprite, -self.direction)
        _rect = _rotated.get_rect(center=(self.x - camera.x + camera.shake_x, self.y - camera.y + camera.shake_y))
        self._window.blit(_rotated, _rect.topleft)

class EnemyProjectile(Projectile):
    def __init__(self, window, x, y, width, height, direction, speed, drag, damage, add_x_velocity = 0, add_y_velocity = 0):
        super().__init__(window, "assets/images/enemyprojectile.png", x, y, width, height, direction, speed, drag, damage, add_x_velocity, add_y_velocity)
        self.type = "EnemyProjectile"

    def update(self, data):
        if self.type == "EnemyProjectile":
            for instance in data["instances"].all_instances:
                if instance.type == "Player":
                    if self.get_collision(instance) and not instance.invulnerable:
                        self.remove = True
                    # if colliding with the player, remove itself.

                elif instance.type == "Parry":
                    if self.get_collision(instance):
                        self.type = "Projectile"
                        self.parried = True
                        self.damage = 100
                        self.speed *= 2
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        self.direction = math.degrees(math.atan2(mouse_y + data["camera"].y - self.y, mouse_x + data["camera"].x - self.x))
                        # changes how the projectile behaves.

                        data["instances"].add_TextDisplay(self._window, instance.x, instance.y, "+PARRY!", 24, (0, 0, 0), None, random.randint(60, 120), 10, 0.9, 1000)
                        for i in range(5):
                            data["instances"].add_ProjectileParticle(self._window, "assets/images/enemyprojectile.png", instance.x, instance.y, 12, 12, random.randint(0, 360), 15, 1, 250)
                        data["camera"].add_shake(20)
                        # visual effects.
                        
                        data["score"] += 20
                        data["ui"].add_TextParticle("ScoreParticle", self._window, random.randint(10, 150), data["height"] - 50, 24, "+20", (0, 0, 0), None, 1000, random.randint(-1, 1), random.randint(-10, -5))
                        for element in data["ui"].ui_list:
                            if element.name == "ScoreText":
                                element.set_text("Score: " + str(data["score"]))
                        # score effects.
        
        elif self.type == "Projectile":
            super().update(data)

    def tick(self, data):
        super().tick(data)
        data["instances"].add_AfterImage(self._window, self.spritepath, self.x, self.y, self.width, self.height, 0, 250, 125, -1)

class Beam(Projectile):
    def __init__(self, window, x, y, width, height, direction, damage):
        super().__init__(window, "assets/images/placeholder.png", x, y, width, height, direction, height if height <= width else width, 1, damage)
        self.x_init = self.x
        self.y_init = self.y
        self._collision = False
        self.can_pre_update = True
        self.always_render = True

        self.velocity_x = self.speed * math.cos(math.radians(self.direction))
        self.velocity_y = self.speed * math.sin(math.radians(self.direction))

    def pre_update(self, data):
        if self._collision:
            self.remove = True
            pass
        
        for instance in data["instances"].all_instances:
            if instance.type == "Enemy" or instance.type == "ProjectileEnemy" or instance.type == "ChargerEnemy":
                if self.get_collision(instance):
                    self._collision = True

            if self.get_room_collision_x(data["room"]) or self.get_room_collision_y(data["room"]):
                self._collision = True

        while not self._collision:
            for instance in data["instances"].all_instances:
                if instance.type == "Enemy" or instance.type == "ProjectileEnemy" or instance.type == "ChargerEnemy":
                    if self.get_collision(instance):
                        self._collision = True
                    # if colliding with an enemy, remove itself.

            if self.get_room_collision_x(data["room"]) or self.get_room_collision_y(data["room"]):
                self._collision = True
            # if colliding with room bounds, remove itself.

            self.x += self.velocity_x
            self.y += self.velocity_y

        self.velocity_x = math.cos(math.radians(self.direction))
        self.velocity_y = math.sin(math.radians(self.direction))

        while self._collision:
            self.x -= self.velocity_x
            self.y -= self.velocity_y
            self._collision = False

            for instance in data["instances"].all_instances:
                if instance.type == "Enemy" or instance.type == "ProjectileEnemy" or instance.type == "ChargerEnemy":
                    if self.get_collision(instance):
                        self._collision = True

            if self.get_room_collision_x(data["room"]) or self.get_room_collision_y(data["room"]):
                self._collision = True

        self.x += self.velocity_x
        self.y += self.velocity_y
        self._collision = True

    def update(self, data):
        pass

    def tick(self, data):
        if self.remove:
            data["instances"].add_BeamFade(self._window, self.x_init, self.y_init, self.x, self.y, self.width, self.height, 50)
            # creates a beam fading effect on its position.

    def render(self, camera):
        pygame.draw.line(self._window, (255, 0, 255), (self.x_init - camera.x + camera.shake_x, self.y_init - camera.y + camera.shake_y), (self.x - camera.x + camera.shake_x, self.y - camera.y + camera.shake_y), self.width)
        pygame.draw.circle(self._window, (255, 0, 255), (self.x - camera.x + camera.shake_x, self.y - camera.y + camera.shake_y), self.width / 2)