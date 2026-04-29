import pygame

pygame.init()

class Effect:
    def __init__(self, window, sprite, width, height, duration):
        self._window = window
        self.width = width
        self.height = height
        self.duration = duration
        self._sprite = pygame.image.load(sprite).convert_alpha()
        self._sprite = pygame.transform.scale(self._sprite, (self.width, self.height))
        self._init_ticks = pygame.time.get_ticks()
        self._alpha = 255

    def render(self):
        self._sprite.set_alpha(125 - round(125 * ((pygame.time.get_ticks() - self._init_ticks) / self.duration)))
        self._window.blit(self._sprite, (0, 0))