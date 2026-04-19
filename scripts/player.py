from scripts.instance import Instance
from scripts.enemy import Enemy
import pygame

pygame.init()

class Player(Instance):

    def __init__(self, window, x, y, width, height, room_width, room_height, health: int, speed: int):
        super().__init__(window, x, y, width, height, room_width, room_height)
        self.health = health
        self.speed = speed

        self._dx = 0
        self._dy = 0
        self.x_velocity = 0
        self.y_velocity = 0
    
    def update(self, instance_list): 
        for instance in instance_list: # check for interactions with other instances
            if isinstance(instance, Enemy):
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
        else:
            self.x_velocity = 0
            self.y_velocity = 0
        self.x += self.x_velocity
        self.y += self.y_velocity
        if self.x > self._room_width / 2 or self.x < -self._room_width / 2:
            self.x -= self.x_velocity
        if self.y > self._room_height / 2 or self.y < -self._room_height / 2:
            self.y -= self.y_velocity
        
    def render(self, camera_x, camera_y):
        pygame.draw.circle(self._window, (0, 0, 255), (self.x - camera_x, self.y - camera_y), self.width)
