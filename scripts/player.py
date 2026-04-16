from scripts.instance import Instance
import pygame

pygame.init()

class Player(Instance):

    def __init__(self, window, x, y, width, height, speed: int):
        super().__init__("Player", window, x, y, width, height)
        self.speed = speed

        self._dx = 0
        self._dy = 0
        self.x_velocity = 0
        self.y_velocity = 0
    
    def update(self, instance_list): 
        for instance in instance_list: # check for interactions with other instances
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
        pygame.draw.circle(self._window, (0, 0, 255), (self.x - camera_x, self.y - camera_y), self.width)
