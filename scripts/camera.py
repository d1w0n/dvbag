import random

class Camera:
    def __init__(self, window, x, y, width, height, smoothing):
        self._window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.smoothing = smoothing
        self.shake = {}
        self.target_x = 0
        self.target_y = 0
        self.shake_amp = 0
        self.shake_x = 0
        self.shake_y = 0

    def add_shake(self, decay, amplitude): 
        if not decay in self.shake.keys(): self.shake[decay] = 0
        self.shake[decay] += amplitude

    def shake_decay(self): 
        for decay_entry in self.shake.keys(): self.shake[decay_entry] *= decay_entry

    def target(self, x, y):
        self.target_x = x
        self.target_y = y
        self.x += (self.target_x - self.x) * self.smoothing
        self.y += (self.target_y - self.y) * self.smoothing

    def random_shake(self):
        self.shake_x = 0
        self.shake_y = 0
        for decay_entry in self.shake.keys():
            self.shake_x += random.randint(-round(self.shake[decay_entry]), round(self.shake[decay_entry]))
            self.shake_y += random.randint(-round(self.shake[decay_entry]), round(self.shake[decay_entry]))