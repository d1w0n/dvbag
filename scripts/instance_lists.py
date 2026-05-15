import pygame
import random
import csv
import sys
import os
import math

from config import BASE_DIR
from scripts.room import Room
from scripts.camera import Camera
from scripts.player import Player
from scripts.enemy import Enemy, ProjectileEnemy, ChargerEnemy
from scripts.projectile import Projectile, Parry, EnemyProjectile, Beam
from scripts.particle import Particle, EnemyParticle, ProjectileParticle, ParryFlash, AfterImage, TextDisplay
from scripts.screen_effects import Effect
from scripts.ui import Bar, Text, TextParticle

class InstanceLists:
    def __init__(self):
        self.type = "InstanceLists"
        self.all_instances = []
        self.remove_instances = []
        self.add_instances = []