import pygame
import random

pygame.init()

class Player:

    def __init__(self, window, x, y, speed = 5):
        self.window = window
        self.x = x
        self.y = y
        
        # optional arguments
        self.speed = speed

        self._dx = 0
        self._dy = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self.type = "Player"
    
    def update(self, instance_list): 
        self._instance_list = instance_list
        for instance in self._instance_list: # check for interations with other instances
            if instance.type == "Enemy":
                pass
        
        # player movement   
        key = pygame.key.get_pressed()

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

    def tick(self):
        self._target_distance = (self._dx ** 2 + self._dy ** 2) ** 0.5 # calculate distance to target using pythagorean theorem
        if self._target_distance > 0:
            self.x_velocity = self._dx / self._target_distance * self.speed
            self.y_velocity = self._dy / self._target_distance * self.speed
            self.x += self.x_velocity
            self.y += self.y_velocity
        
    def render(self, camera_x, camera_y):
        pygame.draw.circle(self.window, (0, 0, 255), (self.x - camera_x, self.y - camera_y), 15)
