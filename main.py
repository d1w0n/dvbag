import time
_start_time = time.perf_counter()
print("\nLoading...")

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
from scripts.list_sort import render_sort

pygame.init()

width, height = 800, 600
window = pygame.display.set_mode([width, height])
# creates a window with the specified width and height.

running = True
clock = pygame.time.Clock()
tickrate = 60
removals = 0

menu_running = True
menu_skip = False
# initializes crucial variables for all loops.

menu_ui = [Text("Title", window, 0, 0, 96, "game_test", (0, 0, 0))]
# initializes menu ui.

print("Loaded. (" + str(time.perf_counter() - _start_time) + " seconds)")

while menu_running and not menu_skip:
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        running = False
        menu_running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((255, 255, 255))

    if pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_SPACE]:
        menu_running = False

    removals = 0
    for i in range(len(menu_ui)):
        if menu_ui[i - removals].remove:
            menu_ui.pop(i - removals)
            removals += 1
        else:
            menu_ui[i - removals].render()
    # removes ui elements that need to be removed.

    pygame.display.flip()

    clock.tick(tickrate)
# menu loop.

_start_time = time.perf_counter()
print("\nLoading save...")

enemy_ticks = 0
projectile_enemy_ticks = 0
score = 0

_save_has_player = False
# main gameplay loop variables.

room = Room(width * 2, height * 2)
camera = Camera(window, -width / 2, -height / 2, width, height, 0.1, 0.8)
# initializes variables from camera and room classes.

all_instances = []
remove_instances = []
add_instances = []
ui = [Bar("HealthBar", window, 0, 0, width, 50, (0, 255, 0)), 
      Text("HealthText", window, 10, 60, 36, "", (0, 255, 0)),
      Text("ScoreText", window, 10, height - 50, 48, "", (0, 0, 0))]
# initialize instance lists.

save_path = os.path.join(BASE_DIR, "saves", "save.csv")

if os.path.exists(save_path):
    with open(save_path, "r") as save:
        csv_reader = csv.DictReader(save)
        for row in csv_reader:
            if row["instance"] == "Player":
                _save_has_player = True
                all_instances.append(Player(window, float(row["x"]), float(row["y"]), 48, 48, 100, 5))
                camera.x = float(row["x"]) - width / 2
                camera.y = float(row["y"]) - height / 2
            # sets player position to saved position.

            elif row["instance"] == "Enemy":
                all_instances.append(Enemy(window, float(row["x"]), float(row["y"]), 48, 48, 100, 3, 10))

            elif row["instance"] == "ProjectileEnemy":
                all_instances.append(ProjectileEnemy(window, float(row["x"]), float(row["y"]), 48, 48, random.randint(70, 100), random.randint(3, 5), 10, 300, 1000))
# if there is a save file, load the instances with their positions from there.

else:
    print("Save file not found. Creating new save file...")
    open(save_path, mode="w", newline="")
# creates a new save file if the file is not found. (usually happens when cloning the github repository.)

if not _save_has_player:
    all_instances = [Player(window, 0, 0, 48, 48, 100, 5), Enemy(window, room.width / 4, 0, 48, 48, 100, 3, 10)]
# if the player was removed in the save, start from a clean slate.

print("Loaded. (" + str(time.perf_counter() - _start_time) + " seconds)")
# prints successful load with elapsed time.

while running:
# main loop.

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # checks for quit events and if the escape key is pressed to end the program.

    window.fill((255, 255, 255))
    # fills the window with white color to clear previous frames.

    mouse_x, mouse_y = pygame.mouse.get_pos()
    # gets the current position of the mouse cursor.

    camera.shake_decay()
    # multiplies camera shake attributes by its decay.

    for instance in add_instances:
        all_instances.append(instance)
    add_instances = []
    # adds queued instances to the instance list, then clears the add instances list.
    
    for instance in all_instances:
        if instance.can_pre_update:
            instance.pre_update(all_instances, room, camera)
    # runs pre-update for instances that have that priority.

    for instance in all_instances:
        instance.update(all_instances, room, camera)
    # updates each instance before doing anything.

        if instance.add_score > 0:
            score += instance.add_score
            ui.append(TextParticle("ScoreParticle", window, random.randint(10, 150), height - 50, 24, "+" + str(instance.add_score), (0, 0, 0), None, 1000, random.randint(-1, 1), random.randint(-10, -5)))
            instance.add_score = 0
        # adds instance add score to score and creates a text particle with score added.

    if (pygame.time.get_ticks() - enemy_ticks) > 3000: 
        enemy_ticks = pygame.time.get_ticks()
        add_instances.append(ChargerEnemy(window, random.randint(round(-room.width / 2), round(room.width / 2)), random.randint(round(-room.height / 2), round(room.height / 2)), 48, 48, random.randint(70, 100), random.randint(5, 7), 10, 200))
    # every second, create an enemy instance at a random position in the room with random health and speed.

    if (pygame.time.get_ticks() - projectile_enemy_ticks) > 3000: 
        projectile_enemy_ticks = pygame.time.get_ticks()
        add_instances.append(ProjectileEnemy(window, random.randint(round(-room.width / 2), round(room.width / 2)), random.randint(round(-room.height / 2), round(room.height / 2)), 48, 48, random.randint(70, 100), random.randint(3, 5), 10, 300, 1000))
    # every second, create a projectile enemy instance at a random position in the room with random health and speed.

    for i in range(len(all_instances)):
        if all_instances[i].remove:
            remove_instances.append(i)
    # if an instance needs to be removed, its index will be appended to the remove instance list and skips next actions.

    for instance in all_instances:
        instance.tick() 
    # performs instances next action after updating.

        if instance.type == "Player":
            camera.target(instance.x - width / 2 + (mouse_x - width / 2) / 4, instance.y - height / 2 + (mouse_y - height / 2) / 4)
            for element in ui:
                if element.name == "HealthBar":
                    element.stat = instance.health
                if element.name == "HealthText":
                    element.set_text("Health: " + str(instance.health) + "")
        # smooths camera position to mouse and player position.

        elif (instance.type == "Enemy" or instance.type == "ProjectileEnemy" or instance.type == "ChargerEnemy") and instance.remove:
            for i in range(5):
                add_instances.append(EnemyParticle(window, instance.x, instance.y, 24, 24, random.randint(5, 10), random.randint(1, 360), 3000))
        # create 5 particles on death. 

        if instance.type == "Player":
            if pygame.mouse.get_pressed()[0] and (pygame.time.get_ticks() - instance.projectile_ticks) > instance.projectile_cooldown:
                instance.projectile_ticks = pygame.time.get_ticks()
                add_instances.append(Projectile(window, instance.x, instance.y, 24, 24, mouse_x + camera.x, mouse_y + camera.y, 24, 25))
                for i in range(3):
                    add_instances.append(ProjectileParticle(window, instance.x, instance.y, 12, 12, "assets/images/dot.png", 15, math.degrees(math.atan2(mouse_y + camera.y - instance.y, mouse_x + camera.x - instance.x)) + random.randint(-45, 45), 250))
                camera.shake(7, 7)
            # if mouse is down, create a projectile instance at player position going towards mouse position, then shake the camera by 5.
            
            if pygame.mouse.get_pressed()[2] and (pygame.time.get_ticks() - instance.beam_ticks) > instance.beam_cooldown:
                instance.beam_ticks = pygame.time.get_ticks()
                add_instances.append(Beam(window, instance.x, instance.y, 24, 24, mouse_x + camera.x, mouse_y + camera.y, 15))
                for i in range(3):
                    add_instances.append(ProjectileParticle(window, instance.x, instance.y, 12, 12, "assets/images/magentadot.png", 20, math.degrees(math.atan2(mouse_y + camera.y - instance.y, mouse_x + camera.x - instance.x)) + random.randint(-45, 45), 150))
                camera.shake(5, 5)
            # creates a beam instead.

            if pygame.key.get_pressed()[pygame.K_f] and (pygame.time.get_ticks() - instance.parry_ticks) > instance.parry_cooldown:
                instance.parry_ticks = pygame.time.get_ticks()
                add_instances.append(Parry(window, instance.x, instance.y, 96, 96, "Player", 10))
                camera.shake(10, 10)
            # if f is down, create a parry instance that reflects enemy projectiles and indicated attacks.

        elif instance.type == "ProjectileEnemy":
            if instance.spawn_projectile and (pygame.time.get_ticks() - instance.cooldown_ticks) > instance.projectile_cooldown:
                instance.cooldown_ticks = pygame.time.get_ticks()
                add_instances.append(EnemyProjectile(window, instance.x, instance.y, 24, 24, instance.target_x, instance.target_y, 10, 10))
                for i in range(3):
                    add_instances.append(ProjectileParticle(window, instance.x, instance.y, 12, 12, "assets/images/enemyprojectile.png", 15, math.degrees(math.atan2(instance.target_y - instance.y, instance.target_x - instance.x)) + random.randint(-45, 45), 250))
            # if player is in range, fire a projectile at the player.

        elif instance.type == "ChargerEnemy":
            if instance.spawn_particle:
                for i in range(3):
                    add_instances.append(ParryFlash(window, instance.x, instance.y, 12, 48, random.randint(1, 360), 500, random.randint(-10, 10)))
            if instance.phase == 2:
                add_instances.append(AfterImage(window, instance.spritepath, instance.x, instance.y, instance.width, instance.height, instance._angle, 250, 125, -1.5))
            instance.spawn_particle = False
        # creates parry indicator particles.

        if hasattr(instance, "has_trail"):
            if instance.has_trail:
                add_instances.append(AfterImage(window, instance.spritepath, instance.x, instance.y, instance.width, instance.height, 0, 250, 125, -1))

        if hasattr(instance, "parry_text"):
            if instance.parry_text:
                add_instances.append(TextDisplay(window, instance.x, instance.y, 5, random.randint(60, 120), 1000, 24, "+PARRY!", (0, 0, 0)))
                instance.parry_text = False

    removals = 0
    for index in remove_instances:
        all_instances.pop(index - removals)
        removals += 1
    remove_instances = []
    # removes instances that needs to be deleted from the instances list, then resets the remove instances list.
    
    camera.random_shake()
    # assign camera shake to dedicated random integer attributes for instance rendering.

    room.draw(window, (200, 200, 200), camera.x + camera.shake_random_x, camera.y + camera.shake_random_y)
    # draws the room borders.

    for instance in render_sort(all_instances, camera):
        instance.render(camera.x + camera.shake_random_x, camera.y + camera.shake_random_y) 
    # renders all instances with camera attributes after ticking.

    removals = 0
    for i in range(len(camera.effects)):
        if camera.effects[i - removals].remove:
            camera.effects.pop(i - removals)
            removals += 1
        else:
            camera.effects[i - removals].render
    # renders screen overlay effects.

    removals = 0
    for i in range(len(ui)):
        if ui[i - removals].remove:
            ui.pop(i - removals)
            removals += 1
    # removes ui elements that need to be removed.

    for element in ui:
        if element.name == "ScoreText":
            element.set_text("Score: " + str(score) + "")
        element.render()
    # renders ui elements.

    pygame.display.flip()
    # updates the display after rendering all instances.

    clock.tick(tickrate)
    # updates main loop at set tickrate.
# end of main loop.

_start_time = time.perf_counter()
print("\nSaving...")
data = [
    ["instance", "x", "y"]
]
# prepares program data for save after quitting, starts with column labels.

for instance in all_instances:
    data.append([instance.type, int(instance.x), int(instance.y)])
# adds player data to the save.

with open(save_path, mode="w", newline="") as save:
    writer = csv.writer(save)
    writer.writerows(data)
# writes completed data to the save. (currently just acts as placeholder)

print("Saved. (" + str(time.perf_counter() - _start_time) + " seconds)" + ("\n" * 2) + "Program Successfully Ended\n")
# prints successful save with elapsed time.

sys.exit()