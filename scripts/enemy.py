from scripts.instance import Instance
import pygame

pygame.init()

class Enemy(Instance):

    def __init__(self, window, x, y, width, height, health: int, speed: int, damage: int):
        super().__init__("Enemy", window, x, y, width, height)
        self.health = health
        self.speed = speed
        self.damage = damage

        self._x_target = 0
        self._y_target = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self._color = (255, 0, 0)

    def update(self, instance_list, room, camera):
        self._color = (255, self._color[1] * 0.9, self._color[2] * 0.9)
        for instance in instance_list:
            if instance.type == "Player":
                self._x_target = instance.x
                self._y_target = instance.y
                # sets target position to go to the player.
            
            if instance.type == "Projectile":
                if self.get_collision(instance):
                    self.health -= instance.damage
                    self._color = (255, 255, 255)
                # checks for collision with projectiles. if collision is true, subtract health by the projectile damage.

        if self.health <= 0:
            self.remove = True
                
    def tick(self):
        self._dx = self._x_target - self.x
        self._dy = self._y_target - self.y
        self._target_distance = (self._dx ** 2 + self._dy ** 2) ** 0.5 
        # calculate distance to target using pythagorean theorem.
        
        if self._target_distance > 0:
            self.velocity_x = self._dx / self._target_distance * self.speed
            self.velocity_y = self._dy / self._target_distance * self.speed
            self.x += self.velocity_x
            self.y += self.velocity_y
        # moves towards the target position.

    def render(self, camera_x, camera_y):
        pygame.draw.circle(self._window, (self._color[0], round(self._color[1]), round(self._color[2])), (self.x - camera_x, self.y - camera_y), self.width)
