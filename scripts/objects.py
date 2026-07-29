# TODO create object classes. should function similar to room borders.
from abc import ABC, abstractmethod
import pygame

pygame.init()

class Object(ABC):
    def __init__(self):
        pass