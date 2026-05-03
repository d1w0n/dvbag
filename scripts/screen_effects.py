from config import BASE_DIR
import os
import pygame

pygame.init()

class Effect:
    def __init__(self, window, sprite, width, height, duration, intensity):
        self._window = window
        self.width = width
        self.height = height
        self.duration = duration
        self.intensity = intensity
        self._sprite = pygame.image.load(os.path.join(BASE_DIR, *sprite.replace("\\", "/").split("/"))).convert_alpha()
        self._sprite = pygame.transform.scale(self._sprite, (self.width, self.height))
        self._init_ticks = pygame.time.get_ticks()
        self._alpha = 255
        self.remove = False

    def render(self):
        if (pygame.time.get_ticks() - self._init_ticks) > self.duration:
            self.remove = True
            pass
        self._sprite.set_alpha(self.intensity - round(self.intensity * ((pygame.time.get_ticks() - self._init_ticks) / self.duration)))
        self._window.blit(self._sprite, (0, 0))