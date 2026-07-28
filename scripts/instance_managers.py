import pygame
import config

"""
import new instance classes here, then add an add method for it in the instance management methods chunk.
"""
from scripts.player import Player
from scripts.enemy import Enemy, ProjectileEnemy, ChargerEnemy
from scripts.projectile import Projectile, Melee, Parry, EnemyProjectile, Beam, \
    Explosion, BombProjectile
from scripts.particle import Particle, EnemyParticle, ProjectileParticle, ParryFlash, \
    AfterImage, TextDisplay, BeamFade, ExplosionFade

from scripts.ui import Bar, Text, TextParticle, ScreenEffect

pygame.init()

class InstanceLists:
    def __init__(self, all_instances = None):
        self.all_instances = all_instances if all_instances is not None else []
        self.add_instances = []

    def append_queued(self):
        for instance in self.add_instances:
            self.all_instances.append(instance)
        self.add_instances = []
    # adds queued instances from the add_instances list to the all_instances list, then clears the add_instances list.

    def remove_instances(self):
        _remove_list = []
        _remove_count = 0

        for i in range(len(self.all_instances)):
            if self.all_instances[i].remove:
                _remove_list.append(i)

        for index in _remove_list:
            self.all_instances.pop(index - _remove_count)
            _remove_count += 1
    # if an instance needs to be removed, its index will be appended to the remove instances list and the all instances list will be popped from the remove instances list.

    def render_sort(self, camera, *types): # TODO: make it sort based off the arguments in types.
        render_list = [] 
        
        for instance in self.all_instances:
            if not instance.get_out_of_view(camera) or hasattr(instance, "always_render"):
                render_list.append(instance)
                
        return render_list
    # sorts the instance list by specified order in parameters.
    # also checks if the instances are on screen; if not, dont render, unless exeption that always renders.

    def __str__(self):
        _list = []
        for instance in self.add_instances:
            _list.append(str(instance))
        for instance in self.all_instances:
            _list.append(str(instance))

        return str(_list).replace("[", "").replace("]", "").replace("\'", "")
    # prints simplified list of instances in both lists.

    """
    when creating a new instance class, add an add class method to the instance management methods chunk.
    this is so objects can create new instances without having to import them as a way to deal with circular imports.
    """
    def add_Player(self, *args):
        self.add_instances.append(Player(*args))
    def add_Enemy(self, *args):
        self.add_instances.append(Enemy(*args))
    def add_TextDisplay(self, *args):
        self.add_instances.append(TextDisplay(*args))
    def add_ProjectileParticle(self, *args):
        self.add_instances.append(ProjectileParticle(*args))
    def add_Particle(self, *args):
        self.add_instances.append(Particle(*args))
    def add_AfterImage(self, *args):
        self.add_instances.append(AfterImage(*args))
    def add_EnemyParticle(self, *args):
        self.add_instances.append(EnemyParticle(*args))
    def add_Projectile(self, *args):
        self.add_instances.append(Projectile(*args))
    def add_Beam(self, *args):
        self.add_instances.append(Beam(*args))
    def add_Melee(self, *args):
        self.add_instances.append(Melee(*args))
    def add_Parry(self, *args):
        self.add_instances.append(Parry(*args))
    def add_ParryFlash(self, *args):
        self.add_instances.append(ParryFlash(*args))
    def add_ProjectileEnemy(self, *args):
        self.add_instances.append(ProjectileEnemy(*args))
    def add_ChargerEnemy(self, *args):
        self.add_instances.append(ChargerEnemy(*args))
    def add_EnemyProjectile(self, *args):
        self.add_instances.append(EnemyProjectile(*args))
    def add_BeamFade(self, *args):
        self.add_instances.append(BeamFade(*args))
    def add_Explosion(self, *args):
        self.add_instances.append(Explosion(*args))
    def add_ExplosionFade(self, *args):
        self.add_instances.append(ExplosionFade(*args))
    def add_BombProjectile(self, *args):
        self.add_instances.append(BombProjectile(*args))
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

    def __str__(self):
            _list = []
            for element in self.ui_list:
                _list.append(str(element))
    
            return str(_list).replace("[", "").replace("]", "").replace("\'", "")
    # prints simplified list of ui elements.
    
    """
    when creating a new ui element, add an add class method to the ui management methods chunk.
    this is so objects can create new ui without having to import them as a way to deal with circular imports.
    """
    def add_Bar(self, *args):
        self.ui_list.append(Bar(*args))
    def add_Text(self, *args):
        self.ui_list.append(Text(*args))
    def add_TextParticle(self, *args):
        self.ui_list.append(TextParticle(*args))
    def add_ScreenEffect(self, *args):
        self.effects.append(ScreenEffect(*args))
    """
    end of ui management methods chunk.
    """