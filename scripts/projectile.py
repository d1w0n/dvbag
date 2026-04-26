from scripts.instance import Instance
import pygame
import math

pygame.init()

class Projectile(Instance):
    def __init__(self, window, x, y, width, height, target_x, target_y, speed: int, damage: int, add_x_velocity = 0, add_y_velocity = 0):
        super().__init__("Projectile", "assets/images/placeholder_thick.png", window, x, y, width, height)
        self.speed = speed
        self.damage = damage
        self._dx = target_x - self.x
        self._dy = target_y - self.y
        self._magnitude = self.get_distance(self._dx, self._dy)
        self.x_velocity = self._dx / self._magnitude * self.speed + add_x_velocity
        self.y_velocity = self._dy / self._magnitude * self.speed + add_y_velocity

    def update(self, instance_list, room, camera):
        self._room = room
        for instance in instance_list:
            if instance.type == "Enemy" or instance.type == "ProjectileEnemy":
                if self.get_collision(instance):
                    self.remove = True
                # if colliding with an enemy, remove itself.

        if self.get_room_collision_x(room) or self.get_room_collision_y(room):
            self.remove = True
        # if colliding with room bounds, remove itself.

    def tick(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        # change x and y by velocities.

    def render(self, camera_x, camera_y):
        self._window.blit(self._sprite, (self.x - self.width / 2 - camera_x, self.y - self.height / 2 - camera_y))





class Parry(Instance):
    def __init__(self, window, x, y, width, height, target_instance, damage):
        super().__init__(self, "assets/images/placeholder.png", window, x, y, width, height)
        self._target_instance = target_instance
        self.damage = damage
        self._start_ticks = pygame.time.get_ticks()
        self._duration = 250

    def update(self, instance_list, room, camera):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for instance in instance_list:
            if instance.type == self._target_instance:
                self._mouse_dx = mouse_x + camera.x - instance.x
                self._mouse_dy = mouse_y + camera.y - instance.y
                self._target_x = instance.x + self.get_velocity_x(self._mouse_dx, self._mouse_dy, instance.width / 2 + self.width / 2)
                self._target_y = instance.y + self.get_velocity_y(self._mouse_dx, self._mouse_dy, instance.height / 2 + self.height / 2)

        if (pygame.time.get_ticks() - self._start_ticks) > self._duration:
            self.remove = True

    def tick(self):
        self.x = self._target_x
        self.y = self._target_y
        self._angle = -math.degrees(math.atan2(self._mouse_dy, self._mouse_dx))

    def render(self, camera_x, camera_y):
        _rotated = pygame.transform.rotate(self._sprite, self._angle)
        _rect = _rotated.get_rect(center=(self.x - camera_x, self.y - camera_y))
        self._window.blit(_rotated, _rect.topleft)





class EnemyProjectile(Projectile):
    def __init__(self, window, x, y, width, height, target_x, target_y, speed: int, damage: int, add_x_velocity = 0, add_y_velocity = 0):
        super().__init__(window, x, y, width, height, target_x, target_y, speed, damage)
        self.type = "EnemyProjectile"
        self.set_sprite("assets/images/placeholder_red.png")

    def update(self, instance_list, room, camera):
        self._room = room
        for instance in instance_list:
            if instance.type == "Player":
                if self.get_collision(instance):
                    self.remove = True
                # if colliding with an enemy, remove itself.

        if self.get_room_collision_x(room) or self.get_room_collision_y(room):
            self.remove = True
        # if colliding with room bounds, remove itself.





class Beam(Instance):
    def __init__(self, window, x, y, width, height, target_x, target_y, damage: int):
        super().__init__("Beam", "assets/images/placeholder.png", window, x, y, width, height)
        self.speed = height if height <= width else width
        self.damage = damage
        self._dx = target_x - self.x
        self._dy = target_y - self.y
        self.x_velocity = self.get_velocity_x(self._dx, self._dy, self.speed)
        self.y_velocity = self.get_velocity_y(self._dx, self._dy, self.speed)
        self._x_init = self.x
        self._y_init = self.y
        self._collision = False

    def update(self, instance_list, room, camera):
        self._room = room

        if self._collision:
            self.remove = True
            pass

        while not self._collision:
            for instance in instance_list:
                if instance.type == "Enemy" or instance.type == "ProjectileEnemy":
                    if self.get_collision(instance):
                        self._collision = True
                    # if colliding with an enemy, remove itself.

            if self.get_room_collision_x(room) or self.get_room_collision_y(room):
                self._collision = True
            # if colliding with room bounds, remove itself.

            self.x += self.x_velocity
            self.y += self.y_velocity

        self.x_velocity = self.get_velocity_x(self._dx, self._dy, 1)
        self.y_velocity = self.get_velocity_y(self._dx, self._dy, 1)

        while self._collision:
            self.x -= self.x_velocity
            self.y -= self.y_velocity
            self._collision = False

            for instance in instance_list:
                if instance.type == "Enemy" or instance.type == "ProjectileEnemy":
                    if self.get_collision(instance):
                        self._collision = True

            if self.get_room_collision_x(room) or self.get_room_collision_y(room):
                self._collision = True

        self.x += self.x_velocity
        self.y += self.y_velocity
        self._collision = True

    def tick(self):
        pass

    def render(self, camera_x, camera_y):
        #self._window.blit(self._sprite, (self.x - self.width / 2 - camera_x, self.y - self.height / 2 - camera_y))
        pygame.draw.line(self._window, (255, 0, 255), (self._x_init - camera_x, self._y_init - camera_y), (self.x - camera_x, self.y - camera_y), self.width)
        pygame.draw.circle(self._window, (255, 0, 255), (self.x - camera_x, self.y - camera_y), self.width / 2)