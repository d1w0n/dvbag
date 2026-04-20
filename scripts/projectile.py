from scripts.instance import Instance
import pygame

pygame.init()

class Projectile(Instance):
    def __init__(self, window, x, y, width, height, room_width, room_height, target_x, target_y, speed: int, damage: int, add_x_velocity = 0, add_y_velocity = 0):
        super().__init__("Projectile", window, x, y, width, height, room_width, room_height)
        self.speed = speed
        self.damage = damage
        self._dx = target_x - self.x
        self._dy = target_y - self.y
        self._magnitude = self.get_magnitude(self._dx, self._dy)
        self.x_velocity = self._dx / self._magnitude * self.speed + add_x_velocity
        self.y_velocity = self._dy / self._magnitude * self.speed + add_y_velocity

    def update(self, instance_list):
        for instance in instance_list:
            if instance.type == "Enemy":
                if self.get_collision(instance):
                    self.remove = True
                # if colliding with an enemy, remove itself.

        if self.get_room_collision_x() or self.get_room_collision_y():
            self.remove = True
        # if colliding with room bounds, remove itself.

    def tick(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        # change x and y by velocities.

    def render(self, camera_x, camera_y):
        pygame.draw.circle(self._window, (255, 0, 255), (self.x - camera_x, self.y - camera_y), self.width)

class Beam(Projectile): # WIP
    def update(self, instance_list):
        super().update(instance_list)
        
    def tick(self):
        self._x_init = self.x
        self._y_init = self.y
        while not self.get_room_collision_x() and self.get_room_collision_y():
            self.x += self.x_velocity
            self.y += self.y_velocity
        
    def render(self, camera_x, camera_y):
        pygame.draw.line(self._window, (255, 0, 255), (self._x_init - camera_x, self._y_init - camera_y), (self.x - camera_x, self.y - camera_y), self.width)