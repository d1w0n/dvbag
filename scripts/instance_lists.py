import os
import pygame

from scripts.player import Player
from scripts.enemy import Enemy, ProjectileEnemy, ChargerEnemy
from scripts.projectile import Projectile, Parry, EnemyProjectile, Beam
from scripts.particle import Particle, EnemyParticle, ProjectileParticle, \
    ParryFlash, AfterImage, TextDisplay, BeamFade
import config

pygame.init()

class InstanceLists:
    def __init__(self, all_instances = []):
        self.all_instances = all_instances
        self.add_instances = []
        self.remove_instances = []

    def append_queued(self):
        for instance in self.add_instances:
            self.all_instances.append(instance)
        self.add_instances = []
    # adds queued instances from the add_instances list to the all_instances list, then clears the add_instances list.