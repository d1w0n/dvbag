from scripts.instance import Instance
import pygame

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



class Beam(Projectile):
    def update(self, instance_list, room, camera):
        self._instance_list = instance_list
        self._room_width = room.width
        self._room_height = room.height
        super().update(self._instance_list, room, camera)

    def tick(self):
        self._break = False
        self._x_init = self.x
        self._y_init = self.y
        while not self.get_room_collision_x() and not self.get_room_collision_y() and not self._break:
            self.x += self.x_velocity
            self.y += self.y_velocity
            """
            for instance in self._instance_list:
                self._break = self.get_collision(instance)
                if self._break:
                    break
            """
        self.x_velocity = self._dx / self._magnitude * 1
        self.y_velocity = self._dy / self._magnitude * 1
        while self.get_room_collision_x() or self.get_room_collision_y():
            self.x -= self.x_velocity
            self.y -= self.y_velocity
        self.x += self.x_velocity
        self.y += self.y_velocity
            
    def render(self, camera_x, camera_y):
        pygame.draw.line(self._window, (255, 0, 255), (self._x_init - camera_x, self._y_init - camera_y), (self.x - camera_x, self.y - camera_y), self.width)