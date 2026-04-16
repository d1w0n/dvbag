from scripts.instance import Instance
import pygame

pygame.init()

class Projectile(Instance):
    def __init__(self, window, x, y, width, height, target_location: tuple, speed: int, damage: int):
        super().__init__("Projectile", window, x, y, width, height)
        self.speed = speed
        self.damage = damage
        self._dx = target_location[0] - self.x
        self._dy = target_location[1] - self.y
        self.x_velocity = self._dx / (self._dx ** 2 + self._dy ** 2) ** 0.5 * self.speed
        self.y_velocity = self._dy / (self._dx ** 2 + self._dy ** 2) ** 0.5 * self.speed

    def update(self, instance_list):
        for instance in instance_list:
            if instance.type == "Enemy":
                pass #self.delete = True

    def tick(self):
            self.x += self.x_velocity
            self.y += self.y_velocity

    def render(self, camera_x, camera_y):
        pygame.draw.circle(self._window, (255, 0, 255), (self.x - camera_x, self.y - camera_y), self.width)