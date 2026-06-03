from scripts.instance import Instance
import pygame
import math
import random

pygame.init()

class Projectile(Instance):
    def __init__(self, window, x, y, width, height, target_x, target_y, speed: int, damage: int, add_x_velocity = 0, add_y_velocity = 0):
        super().__init__("Projectile", "assets/images/placeholder.png", window, x, y, width, height)
        self.parried = False
        self.damage = damage
        self.speed = speed
        self.velocity_x, self.velocity_y = self.get_velocity(target_x - self.x, target_y - self.y, self.speed)

    def update(self, data):
        self._room = data["room"]
        for instance in data["instances"].all_instances:
            if instance.type == "Enemy" or instance.type == "ProjectileEnemy" or instance.type == "ChargerEnemy":
                if self.get_collision(instance):
                    self.remove = True
                # if colliding with an enemy, remove itself.

        if self.get_room_collision_x(data["room"]) or self.get_room_collision_y(data["room"]):
            self.remove = True
        # if colliding with room bounds, remove itself.

    def tick(self, data):
        self.x += self.velocity_x
        self.y += self.velocity_y
        # change x and y by velocities.

    def render(self, camera):
        self._window.blit(self._sprite, (self.x - self.width / 2 - camera.x + camera.shake_x, self.y - self.height / 2 - camera.y + camera.shake_y))



class Parry(Instance):
    def __init__(self, window, x, y, width, height, target_instance, damage):
        super().__init__("Parry", "assets/images/placeholder.png", window, x, y, width, height)
        self._target_instance = target_instance
        self.damage = damage
        self.start_ticks = pygame.time.get_ticks()
        self._duration = 250
        self._has_target = False

    def update(self, data):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self._has_target = False
        for instance in data["instances"].all_instances:
            if instance.type == self._target_instance:
                self._mouse_dx = mouse_x + data["camera"].x - instance.x
                self._mouse_dy = mouse_y + data["camera"].y - instance.y
                self._target_x, self._target_y = self.get_velocity(self._mouse_dx, self._mouse_dy, instance.width / 2)
                self._target_x += instance.x
                self._target_y += instance.y
                self._has_target = True

            elif instance.type == "EnemyProjectile" or (instance.type == "Projectile" and instance.parried) or instance.type == "ChargerEnemy":
                if self.get_collision(instance):
                    self.remove = True
        
        if not self._has_target:
            self.remove = True
                
        if (pygame.time.get_ticks() - self.start_ticks) > self._duration:
            self.remove = True

    def tick(self, data):
        self.x = self._target_x
        self.y = self._target_y
        self._angle = -math.degrees(math.atan2(self._mouse_dy, self._mouse_dx))

    def render(self, camera):
        _rotated = pygame.transform.rotate(self._sprite, self._angle)
        _rect = _rotated.get_rect(center=(self.x - camera.x + camera.shake_x, self.y - camera.y + camera.shake_y))
        self._window.blit(_rotated, _rect.topleft)





class EnemyProjectile(Projectile):
    def __init__(self, window, x, y, width, height, target_x, target_y, speed: int, damage: int, add_x_velocity = 0, add_y_velocity = 0):
        super().__init__(window, x, y, width, height, target_x, target_y, speed, damage)
        self.type = "EnemyProjectile"
        self.parry_text = False
        self.set_sprite("assets/images/enemyprojectile.png")

    def update(self, data):
        if self.type == "EnemyProjectile":
            self._room = data["room"]
            for instance in data["instances"].all_instances:
                if instance.type == "Player":
                    if self.get_collision(instance):
                        self.remove = True
                    # if colliding with an enemy, remove itself.

                elif instance.type == "Parry":
                    if self.get_collision(instance):
                        data["instances"].add_TextDisplay(self._window, instance.x, instance.y, 5, random.randint(60, 120), 1000, 24, "+PARRY!", (0, 0, 0))
                        for i in range(5):
                            data["instances"].add_ProjectileParticle(self._window, instance.x, instance.y, 12, 12, "assets/images/enemyprojectile.png", 15, random.randint(0, 360), 250)
                        data["camera"].add_shake(20)

                        self.type = "Projectile"
                        self.parried = True
                        self.damage = 100
                        data["score"] += 20
                        data["ui"].add_TextParticle("ScoreParticle", self._window, random.randint(10, 150), data["height"] - 50, 24, "+20", (0, 0, 0), None, 1000, random.randint(-1, 1), random.randint(-10, -5))
                        for element in data["ui"].ui_list:
                            if element.name == "ScoreText":
                                element.set_text("Score: " + str(data["score"]))
                        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                        self.velocity_x, self.velocity_y = self.get_velocity((self.mouse_x + data["camera"].x) - self.x, (self.mouse_y + data["camera"].y) - self.y, self.speed * 2)
        
        elif self.type == "Projectile":
            super().update(data)

        if self.get_room_collision_x(data["room"]) or self.get_room_collision_y(data["room"]):
            self.remove = True
        # if colliding with room bounds, remove itself.

    def tick(self, data):
        super().tick(data)
        data["instances"].add_AfterImage(self._window, self.spritepath, self.x, self.y, self.width, self.height, 0, 250, 125, -1)





class Beam(Instance):
    def __init__(self, window, x, y, width, height, target_x, target_y, damage: int):
        super().__init__("Beam", "assets/images/placeholder.png", window, x, y, width, height)
        self.speed = height if height <= width else width
        self.damage = damage
        self._dx = target_x - self.x
        self._dy = target_y - self.y
        self.velocity_x, self.velocity_y = self.get_velocity(self._dx, self._dy, self.speed)
        self.x_init = self.x
        self.y_init = self.y
        self._collision = False
        self.can_pre_update = True
        self.always_render = True

    def pre_update(self, data):
        self._room = data["room"]
        if self._collision:
            self.remove = True
            pass
        
        for instance in data["instances"].all_instances:
            if instance.type == "Enemy" or instance.type == "ProjectileEnemy" or instance.type == "ChargerEnemy":
                if self.get_collision(instance):
                    self._collision = True

            if self.get_room_collision_x(data["room"]) or self.get_room_collision_y(data["room"]):
                self._collision = True

        if not self._collision:
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

            self.velocity_x, self.velocity_y = self.get_velocity(self._dx, self._dy, 1)

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