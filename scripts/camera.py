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
        self.shake_amp = 0
        self.shake_x = 0
        self.shake_y = 0

    def add_shake(self, amplitude):
        self.shake_amp += amplitude

    def shake_decay(self):
        self.shake_amp *= self.decay

    def target(self, x, y):
        self.target_x = x
        self.target_y = y
        self.x += (self.target_x - self.x) * self.smoothing
        self.y += (self.target_y - self.y) * self.smoothing

    def random_shake(self):
        self.shake_x = random.randint(-round(self.shake_amp), round(self.shake_amp))
        self.shake_y = random.randint(-round(self.shake_amp), round(self.shake_amp))