import random
from scripts.screen_effects import Effect

class Camera:
    def __init__(self, window, x, y, width, height, smoothing, decay):
        self._window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.smoothing = smoothing
        self.decay = decay
        
        self.target_x = 0
        self.target_y = 0
        self.shake_x_abs = 0
        self.shake_y_abs = 0
        self.shake_random_x = 0
        self.shake_random_y = 0    
        self.effects = []

    def shake(self, x, y):
        self.shake_x_abs += x
        self.shake_y_abs += y

    def shake_decay(self):
        self.shake_x_abs *= self.decay
        self.shake_y_abs *= self.decay

    def target(self, x, y):
        self.target_x = x
        self.target_y = y
        self.x += (self.target_x - self.x) * self.smoothing
        self.y += (self.target_y - self.y) * self.smoothing

    def random_shake(self):
        self.shake_x = random.randint(-round(self.shake_x_abs), round(self.shake_x_abs))
        self.shake_y = random.randint(-round(self.shake_y_abs), round(self.shake_y_abs))

    def add_effect(self, sprite, duration, intensity):
        self.effects.append(Effect(self._window, sprite, self.width, self.height, duration, intensity))