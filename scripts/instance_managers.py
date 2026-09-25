import pygame
import config
import math

"""
import new instance classes here, then add an add method for it in the instance management methods chunk.
"""
from scripts.player import Player
from scripts.enemies import Enemy, ProjectileEnemy, ChargerEnemy
from scripts.projectiles import Projectile, Melee, Parry, EnemyProjectile, Beam, \
    Explosion, BombProjectile
from scripts.particles import Particle, EnemyParticle, ProjectileParticle, ParryFlash, \
    AfterImage, TextDisplay, BeamFade, ExplosionFade

from scripts.ui import Bar, Text, TextParticle, ScreenEffect

from scripts.objects import Wall

pygame.init()

class InstanceLists:
    def __init__(self, *args):
        self.all_instances = {}
        self.add_instances = []
        self.grid = {}
        for supertype in args: self.all_instances[supertype] = []

    def append_queued(self):
        for instance in self.add_instances:
            try: self.all_instances[instance.supertype].append(instance)
            except KeyError: raise KeyError("Appended instance supertype was not defined in InstanceLists initialization. (instance supertype: " + instance.supertype + ")")
            
        self.add_instances = []
    # adds queued instances to the instance lists, then clears the add_instances list.

    def remove_instances(self):
        for supertype in self.all_instances.keys():
            _remove_list = []
            for i in range(len(self.all_instances[supertype])):
                if self.all_instances[supertype][i].remove: _remove_list.append(i)

            _remove_count = 0
            for index in _remove_list:
                self.all_instances[supertype].pop(index - _remove_count)
                _remove_count += 1
    # if an instance needs to be removed, its index will be appended to the remove instances list and the all instances list will be popped from the remove instances list.

    def create_grid(self):
        self.grid = {}
        for supertype in self.all_instances.keys():
            for instance in self.all_instances[supertype]:
                cell = (math.floor(instance.x / 64), math.floor(instance.y / 64))
                if cell not in self.grid: self.grid[cell] = []
                self.grid[cell].append(instance)

    def get_cell(self, x, y) -> list:
        return self.grid[(math.floor(x / 64), math.floor(y / 64))]

    def get_nearby(self, x, y) -> dict:
        cell_x = math.floor(x / 64)
        cell_y = math.floor(y / 64)
        _nearby = {}
        for supertype in self.all_instances.keys(): _nearby[supertype] = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (cell_x + dx, cell_y + dy) in self.grid:
                    for instance in self.grid[(cell_x + dx, cell_y + dy)]: _nearby[instance.supertype].append(instance)

        return _nearby
            
    def __str__(self):
        _list = []
        for instance in self.add_instances: _list.append(str(instance))
        for supertype in self.all_instances.keys():
            for instance in self.all_instances[supertype]:  _list.append(str(instance))

        return str(_list).replace("[", "").replace("]", "").replace("\'", "")
    # prints simplified list of instances in both lists.

    """
    when creating a new instance class, add an add class method to the instance management methods chunk.
    this is so objects can create new instances without having to import them as a way to deal with circular imports.
    """
    def add_Player(self, *args): self.add_instances.append(Player(*args))
    def add_Enemy(self, *args): self.add_instances.append(Enemy(*args))
    def add_TextDisplay(self, *args): self.add_instances.append(TextDisplay(*args))
    def add_ProjectileParticle(self, *args): self.add_instances.append(ProjectileParticle(*args))
    def add_Particle(self, *args): self.add_instances.append(Particle(*args))
    def add_AfterImage(self, *args): self.add_instances.append(AfterImage(*args))
    def add_EnemyParticle(self, *args): self.add_instances.append(EnemyParticle(*args))
    def add_Projectile(self, *args): self.add_instances.append(Projectile(*args))
    def add_Beam(self, *args): self.add_instances.append(Beam(*args))
    def add_Melee(self, *args): self.add_instances.append(Melee(*args))
    def add_Parry(self, *args): self.add_instances.append(Parry(*args))
    def add_ParryFlash(self, *args): self.add_instances.append(ParryFlash(*args))
    def add_ProjectileEnemy(self, *args): self.add_instances.append(ProjectileEnemy(*args))
    def add_ChargerEnemy(self, *args): self.add_instances.append(ChargerEnemy(*args))
    def add_EnemyProjectile(self, *args): self.add_instances.append(EnemyProjectile(*args))
    def add_BeamFade(self, *args): self.add_instances.append(BeamFade(*args))
    def add_Explosion(self, *args): self.add_instances.append(Explosion(*args))
    def add_ExplosionFade(self, *args): self.add_instances.append(ExplosionFade(*args))
    def add_BombProjectile(self, *args): self.add_instances.append(BombProjectile(*args))
    """
    end of instance management methods chunk.
    """

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

            else: self.ui_list[i - self._removals].render()
    # removes ui elements that need to be removed; else render the ui element.

    def effects_render(self):
        self._removals = 0
        for i in range(len(self.effects)):
            if self.effects[i - self._removals].remove:
                self.effects.pop(i - self._removals)
                self._removals += 1

            else: self.effects[i - self._removals].render()
    # renders screen overlay effects.

    def __str__(self):
        _list = []
        for element in self.ui_list: _list.append(str(element))

        return str(_list).replace("[", "").replace("]", "").replace("\'", "")
    # prints simplified list of ui elements.
    
    """
    when creating a new ui element, add an add class method to the ui management methods chunk.
    this is so objects can create new ui without having to import them as a way to deal with circular imports.
    """
    def add_Bar(self, *args): self.ui_list.append(Bar(*args))
    def add_Text(self, *args): self.ui_list.append(Text(*args))
    def add_TextParticle(self, *args): self.ui_list.append(TextParticle(*args))
    def add_ScreenEffect(self, *args): self.effects.append(ScreenEffect(*args))
    """
    end of ui management methods chunk.
    """

class ObjectList:
    def __init__(self, object_list = None):
        self.object_list = object_list if object_list is not None else []
        self.add_objects = []

    def append_objects(self):
        for object in self.add_objects: self.object_list.append(object)
        self.add_objects = []

    def remove_objects(self):
        _remove_list = []
        _remove_count = 0
        for i in range(len(self.object_list)):
            if self.object_list[i].remove: _remove_list.append(i)

        for index in _remove_list:
            self.object_list.pop(index - _remove_count)
            _remove_count += 1

    def render_objects(self, camera):
        for object in self.object_list: object.render(camera)
    # TODO implement objects not rendering if off camera (like how instances do)

    def __str__(self):
        _list = []
        for object in self.add_objects: _list.append(str(object))
        for object in self.add_objects: _list.append(str(object))
        
        return str(_list).replace("[", "").replace("]", "").replace("\'", "")

    """
    object management chunk ig bro
    """
    def add_Wall(self, *args): self.add_objects.append(Wall(*args))
    """
    end of chunk
    """