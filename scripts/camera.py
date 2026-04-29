import random
from scripts.screen_effects import Effect

class Camera:
    def __init__(self, x, y, width, height, smoothing, decay):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.smoothing = smoothing
        self.decay = decay
        
        self.target_x = 0
        self.target_y = 0
        self.shake_x = 0
        self.shake_y = 0
        self.shake_random_x = 0
        self.shake_random_y = 0    
        self.effects = []

    def shake(self, x, y):
        self.shake_x += x
        self.shake_y += y

    def shake_decay(self):
        self.shake_x *= self.decay
        self.shake_y *= self.decay

    def target(self, x, y):
        self.target_x = x
        self.target_y = y
        self.x += (self.target_x - self.x) * self.smoothing
        self.y += (self.target_y - self.y) * self.smoothing

    def random_shake(self):
        self.shake_random_x = random.randint(-round(self.shake_x), round(self.shake_x))
        self.shake_random_y = random.randint(-round(self.shake_y), round(self.shake_y))

    def add_effect(self, window, sprite, duration):
        self.effects.append(Effect(window, sprite, self.width, self.height, duration))