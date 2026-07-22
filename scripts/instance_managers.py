import pygame

import config

"""
import new instance classes here, then add an add method for it in the instance management methods chunk.
"""
from scripts.player import Player
from scripts.enemy import Enemy, ProjectileEnemy, ChargerEnemy
from scripts.projectile import Projectile, Parry, EnemyProjectile, Beam, Explosion
from scripts.particle import Particle, EnemyParticle, ProjectileParticle, ParryFlash, AfterImage, TextDisplay, BeamFade

from scripts.ui import Bar, Text, TextParticle
from scripts.screen_effects import Effect

pygame.init()

class InstanceLists:
    def __init__(self, all_instances = None):
        self.all_instances = all_instances if all_instances is not None else []
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

    def render_sort(self, camera, *types): # TODO: make it sort based off the arguments in types.
        render_list = [] 
        
        for instance in self.all_instances:
            if not instance.get_out_of_view(camera) or hasattr(instance, "always_render"):
                render_list.append(instance)
                
        return render_list
    # sorts the instance list by specified order in parameters.
    # also checks if the instances are on screen; if not, dont render, unless exeption that always renders.

    """
    when creating a new instance class, add an add class method to the instance management methods chunk.
    this is so instances can create new instances without having to import them as a way to deal with circular imports.
    """
    def add_Player(self, window, sprite, x, y, width, height, health, speed):
        self.add_instances.append(Player(window, sprite, x, y, width, height, health, speed))
    def add_Enemy(self, window, sprite, x, y, width, height, health, speed, damage):
        self.add_instances.append(Enemy(window, sprite, x, y, width, height, health, speed, damage))
    def add_TextDisplay(self, window, x, y, text = "", size = 12, color = (0, 0, 0), font = None, direction = 0, speed = 0, drag = 0, duration = 1000):
        self.add_instances.append(TextDisplay(window, x, y, text, size, color, font, direction, speed, drag, duration))
    def add_ProjectileParticle(self, window, sprite, x, y, width, height, direction, speed, drag, duration):
        self.add_instances.append(ProjectileParticle(window, sprite, x, y, width, height, direction, speed, drag, duration))
    def add_Particle(self, window, sprite, x, y, width, height, direction, speed, drag, duration):
        self.add_instances.append(Particle(window, sprite, x, y, width, height, direction, speed, drag, duration))
    def add_AfterImage(self, window, sprite, x, y, width, height, direction, duration, strength, size_change = 0):
        self.add_instances.append(AfterImage(window, sprite, x, y, width, height, direction, duration, strength, size_change))
    def add_EnemyParticle(self, window, x, y, width, height, direction, speed, drag, duration):
        self.add_instances.append(EnemyParticle(window, x, y, width, height, direction, speed, drag, duration))
    def add_Projectile(self, window, sprite, x, y, width, height, direction, speed, drag, damage, add_x_velocity = 0, add_y_velocity = 0):
        self.add_instances.append(Projectile(window, sprite, x, y, width, height, direction, speed, drag, damage, add_x_velocity, add_y_velocity))
    def add_Beam(self, window, x, y, width, height, direction, damage):
        self.add_instances.append(Beam(window, x, y, width, height, direction, damage))
    def add_Parry(self, window, x, y, width, height, target_instance, damage):
        self.add_instances.append(Parry(window, x, y, width, height, target_instance, damage))
    def add_ParryFlash(self, window, x, y, width, height, direction, duration, rotation_speed = 0):
        self.add_instances.append(ParryFlash(window, x, y, width, height, direction, duration, rotation_speed))
    def add_ProjectileEnemy(self, window, x, y, width, height, health, speed, damage, range, cooldown = 1000):
        self.add_instances.append(ProjectileEnemy(window, x, y, width, height, health, speed, damage, range, cooldown))
    def add_ChargerEnemy(self, window, x, y, width, height, health, speed, damage, range):
        self.add_instances.append(ChargerEnemy(window, x, y, width, height, health, speed, damage, range))
    def add_EnemyProjectile(self, window, x, y, width, height, direction, speed, drag, damage, add_x_velocity = 0, add_y_velocity = 0):
        self.add_instances.append(EnemyProjectile(window, x, y, width, height, direction, speed, drag, damage, add_x_velocity, add_y_velocity))
    def add_BeamFade(self, window, x_init, y_init, x, y, width, height, duration):
        self.add_instances.append(BeamFade(window, x_init, y_init, x, y, width, height, duration))
    def add_Explosion(self, window, x, y, radius, duration, damage):
        self.add_instances.append(Explosion(window, x, y, radius, duration, damage))
    # instance management methods chunk.

class UIList:
    def __init__(self, ui_list = None, effects = None):
        self.ui_list = ui_list if ui_list is not None else []
        self.effects = effects if effects is not None else []

    def ui_render(self):
        self._removals = 0
        for i in range(len(self.ui_list)):
            if self.ui_list[i - self._removals].remove:
                self.ui_list.pop(i - self._removals)
                self._removals += 1
            else:
                self.ui_list[i - self._removals].render()
    # removes ui elements that need to be removed; else render the ui element.

    def effects_render(self):
        self._removals = 0
        for i in range(len(self.effects)):
            if self.effects[i - self._removals].remove:
                self.effects.pop(i - self._removals)
                self._removals += 1
            else:
                self.effects[i - self._removals].render()
    # renders screen overlay effects.

    def add_Bar(self, name, window, x, y, width, height, color, stat = 100):
        self.ui_list.append(Bar(name, window, x, y, width, height, color, stat))
    def add_Text(self, name, window, x, y, size, text, color, font = None):
        self.ui_list.append(Text(name, window, x, y, size, text, color, font))
    def add_TextParticle(self, name, window, x, y, size, text, color, font = None, duration = 0, x_velocity = 0, y_velocity = 0):
        self.ui_list.append(TextParticle(name, window, x, y, size, text, color, font, duration, x_velocity, y_velocity))
    def add_Effect(self, window, sprite, width, height, duration, intensity):
        self.effects.append(Effect(window, sprite, width, height, duration, intensity))
    # instance management methods chunk.