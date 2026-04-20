import pygame
import random
from scripts.instance import Instance

pygame.init()

class Particle(Instance):
    def __init__(self, window, x, y, width, height):
        super().__init__("Particle", window, x, y, width, height)