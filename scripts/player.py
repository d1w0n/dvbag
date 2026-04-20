from scripts.instance import Instance
import pygame

pygame.init()

class Player(Instance):

    def __init__(self, window, x, y, width, height, health: int, speed: int):
        super().__init__("Player", window, x, y, width, height)
        self.health = health
        self.speed = speed

        self._dx = 0
        self._dy = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self._color = (0, 0, 255)
        self.cooldown_ticks = 0
        self.projectile_cooldown = 100
        self._damage_cooldown = 1000
        self._damage_ticks = 0
    
    def update(self, instance_list, room, camera): 
        self._room_width = room.width
        self._room_height = room.height
        
        for instance in instance_list:
            if instance.type == "Enemy":
                if self.get_collision(instance) and (pygame.time.get_ticks() - self._damage_ticks) > self._damage_cooldown:
                    self._damage_ticks = pygame.time.get_ticks()
                    self.health -= instance.damage
                    camera.shake(50, 50) 
        
        key = pygame.key.get_pressed()

        self._dx = 0
        self._dy = 0
        # reset target x and y.

        if key[pygame.K_LSHIFT]:
            self.speed = 10
        else:
            self.speed = 5
        if key[pygame.K_w]:
            self._dy = -self.speed
        if key[pygame.K_a]:
            self._dx = -self.speed
        if key[pygame.K_s]:
            self._dy = self.speed
        if key[pygame.K_d]:
            self._dx = self.speed
        # player movement.

    def tick(self):
        self._target_distance = (self._dx ** 2 + self._dy ** 2) ** 0.5 
        # use pythagorean theorem to stop extra diagonal speed.

        if self._target_distance > 0:
            self.x_velocity = self._dx / self._target_distance * self.speed
            self.y_velocity = self._dy / self._target_distance * self.speed
        # sets velocity to move towards the target.

        else:
            self.x_velocity = 0
            self.y_velocity = 0
        # if no movement, set velocity to 0.

        self.x += self.x_velocity
        self.y += self.y_velocity
        # adds x and y by velocities.

        if self.x > self._room_width / 2 or self.x < -self._room_width / 2:
            self.x -= self.x_velocity
        if self.y > self._room_height / 2 or self.y < -self._room_height / 2:
            self.y -= self.y_velocity
        # if colliding with room bounds, revert x or y velocity change.
        
    def render(self, camera_x, camera_y):
        pygame.draw.circle(self._window, self._color, (self.x - camera_x, self.y - camera_y), self.width)