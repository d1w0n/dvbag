from scripts.instance import Instance
import pygame
import math

pygame.init()

class Projectile(Instance):
    def __init__(self, window, x, y, width, height, target_x, target_y, speed: int, damage: int, add_x_velocity = 0, add_y_velocity = 0):
        super().__init__("Projectile", "assets/placeholder_thick.png", window, x, y, width, height)
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
            if instance.type == "Enemy":
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
        super().__init__(self, "assets/placeholder.png", window, x, y, width, height)
        self._target_instance = target_instance
        self.damage = damage

    def update(self, instance_list, room, camera):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for instance in instance_list:
            if instance.type == self._target_instance:
                self._target_x = instance.x + self.get_velocity_x(mouse_x - camera.width / 2, mouse_y - camera.height / 2, instance.width / 2 + self.width / 2)
                self._target_y = instance.y + self.get_velocity_y(mouse_x - camera.width / 2, mouse_y - camera.height / 2, instance.height / 2 + self.height / 2)

    def tick(self):
        self.x = self._target_x
        self.y = self._target_y

    def render(self, camera_x, camera_y):
        self._window.blit(self._sprite, (self.x - self.width / 2 - camera_x, self.y - self.height / 2 - camera_y))