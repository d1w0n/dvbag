import pygame

from scripts.player import Player
from scripts.enemy import Enemy, ProjectileEnemy, ChargerEnemy
from scripts.projectile import Projectile, Parry, EnemyProjectile, Beam
from scripts.particle import Particle, EnemyParticle, ProjectileParticle, ParryFlash, AfterImage, TextDisplay, BeamFade
from scripts.list_sort import render_sort

from scripts.ui import Bar, Text, TextParticle

from scripts.screen_effects import Effect

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

    def queue_removals(self):
        for i in range(len(self.all_instances)):
            if self.all_instances[i].remove:
                self.remove_instances.append(i)
    # if an instance needs to be removed, its index will be appended to the remove instance list.

    def remove_queued(self):
        self._removals = 0
        for index in self.remove_instances:
            self.all_instances.pop(index - self._removals)
            self._removals += 1
        self.remove_instances = []
        del self._removals
    # removes instances that needs to be deleted from the instances list, then resets the remove instances list.

class UIList:
    def __init__(self, ui_list = []):
        self.ui_list = ui_list

    def render(self):
        self._removals = 0
        for i in range(len(self.ui_list)):
            if self.ui_list[i - self._removals].remove:
                self.ui_list.pop(i - self._removals)
                self._removals += 1
            else:
                self.ui_list[i - self._removals].render()
        # removes ui elements that need to be removed; else render the ui element.
"""
class EffectList:
    def __init__(self, effect_list = []):
        self.effect_list = effect_list

    def render(self):
        self._removals = 0
        for i in range(len(self.effects)):
            if self.effects[i - self._removals].remove:
                self.effects.pop(i - self._removals)
                self._removals += 1
            else:
                self.effects[i - self._removals].render()
"""