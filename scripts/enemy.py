from scripts.instance import Instance
import pygame

pygame.init()

class Enemy(Instance):

    def __init__(self, window, x, y, width, height, speed: int):
        super().__init__("Enemy", window, x, y, width, height)
        self.speed = speed

        self._x_target = 0
        self._y_target = 0

    def update(self, instance_list):
        for instance in instance_list:
            if instance.type == "Player":
                self._x_target = instance.x
                self._y_target = instance.y
                
    def tick(self):
        self._dx = self._x_target - self.x
        self._dy = self._y_target - self.y
        self._target_distance = (self._dx ** 2 + self._dy ** 2) ** 0.5 # calculate distance to target using pythagorean theorem
        
        if self._target_distance > 0:
            self.x += self._dx / self._target_distance * self.speed
            self.y += self._dy / self._target_distance * self.speed

    def render(self, camera_x, camera_y):
        pygame.draw.circle(self._window, (255, 0, 0), (self.x - camera_x, self.y - camera_y), self.width)
