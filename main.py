import time
_start_time = time.perf_counter()
print("\nLoading...")

import random
import csv
import sys
import os
import math
try:
    import pygame
except ModuleNotFoundError:
    print("\nPygame is not installed. Please install Pygame! Instructions below.\n \
          1. Open the terminal\n \
          2. Enter this command: \'pip install pygame\'\n \
          3. Retry this program!" + "\n" * 2 + "Program Successfully Ended\n")
    sys.exit()

from scripts.room import Room
from scripts.camera import Camera
from scripts.player import Player
from scripts.enemy import Enemy, ProjectileEnemy, ChargerEnemy
from scripts.projectile import Projectile, Parry, EnemyProjectile, Beam
from scripts.particle import Particle, EnemyParticle, ProjectileParticle, \
    ParryFlash, AfterImage, TextDisplay, BeamFade
from scripts.screen_effects import Effect
from scripts.ui import Bar, Text, TextParticle
from scripts.list_sort import render_sort
import config

pygame.init()

width, height = 800, 600
window = pygame.display.set_mode([width, height])
# creates a window with the specified width and height.

running = True
clock = pygame.time.Clock()
tickrate = 60
removals = 0
menu_running = True
tick_pause = 0
# variable initialization.

data = {
    "ui": [
        Text("Title", window, 0, 0, 96, "this is technically a menu", (0, 0, 0))
    ]
}
# initializes menu data.

print("Loaded. (" + str(time.perf_counter() - _start_time) + " seconds)")

while menu_running and not config.MENU_SKIP:
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
    for i in range(len(data["ui"])):
        if data["ui"][i - removals].remove:
            data["ui"].pop(i - removals)
            removals += 1
        else:
            data["ui"][i - removals].render()
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

data = {
    "room": Room(width * 2, height * 2),
    "camera": Camera(window, -width / 2, -height / 2, width, height, 0.1, 0.8),
    "all_instances": [],
    "remove_instances": [],
    "add_instances": [],
    "ui": [Bar("HealthBar", window, 0, 0, width / 2, 50, (0, 255, 0)), 
        Text("HealthText", window, 10, 60, 36, "", (0, 255, 0)),
        Text("ScoreText", window, 10, height - 50, 48, "", (0, 0, 0))]
}
# initialize main loop data.

save_path = os.path.join(config.BASE_DIR, "saves", "save.csv")
# get save file location.

if os.path.exists(save_path):
    with open(save_path, "r") as save:
        csv_reader = csv.DictReader(save)
        for row in csv_reader:
            if row["instance"] == "Player":
                _save_has_player = True
                data["all_instances"].append(Player(window, float(row["x"]), float(row["y"]), 48, 48, 100, 5))
                data["camera"].x = float(row["x"]) - width / 2
                data["camera"].y = float(row["y"]) - height / 2
            # sets player position to saved position.

            elif row["instance"] == "Enemy":
                data["all_instances"].append(Enemy(window, float(row["x"]), float(row["y"]), 48, 48, 100, 3, 10))

            elif row["instance"] == "ProjectileEnemy":
                data["all_instances"].append(ProjectileEnemy(window, float(row["x"]), float(row["y"]), 48, 48, random.randint(70, 100), random.randint(3, 5), 10, 300, 1000))

            elif row["instance"] == "ChargerEnemy":
                data["all_instances"].append(ChargerEnemy(window, float(row["x"]), float(row["y"]), 48, 48, random.randint(70, 100), random.randint(5, 7), 10, 200))
# if there is a save file, load the instances with their positions from there.

else:
    print("Save file not found. Creating new save file...")
    open(save_path, mode="w", newline="")
# creates a new save file if the file is not found (happens when cloning the github repository.)

if not _save_has_player:
    data["all_instances"] = [
        Player(window, 0, 0, 48, 48, 100, 5), Enemy(window, data["room"].width / 4, 0, 48, 48, 100, 3, 10)
    ]
# if the player was removed in the save, start from a clean slate.

print("Loaded. (" + str(time.perf_counter() - _start_time) + " seconds)")
# prints successful load with elapsed time.

while running:
# main loop; instance management is in here.

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

    data["camera"].shake_decay()
    # multiplies camera shake attributes by its decay.

    for instance in data["add_instances"]:
        data["all_instances"].append(instance)
    data["add_instances"] = []
    # adds queued instances to the instance list, then clears the add instances list.
    
    for instance in data["all_instances"]:
        if instance.can_pre_update:
            instance.pre_update(data["all_instances"], data["room"], data["camera"])
    # runs pre-update for instances that have that priority.

    for instance in data["all_instances"]:
        instance.update(data["all_instances"], data["room"], data["camera"])
    # updates each instance before doing anything.

        if instance.add_score > 0:
            score += instance.add_score
            data["ui"].append(TextParticle("ScoreParticle", window, random.randint(10, 150), height - 50, 24, "+" + str(instance.add_score), (0, 0, 0), None, 1000, random.randint(-1, 1), random.randint(-10, -5)))
            for element in data["ui"]:
                if element.name == "ScoreText":
                    element.set_text("Score: " + str(score) + "")
            instance.add_score = 0
        # adds instance add score to score and creates a text particle with score added.

    if (pygame.time.get_ticks() - enemy_ticks) > 3000: 
        enemy_ticks = pygame.time.get_ticks()
        data["add_instances"].append(ChargerEnemy(window, random.randint(round(-data["room"].width / 2), round(data["room"].width / 2)), random.randint(round(-data["room"].height / 2), round(data["room"].height / 2)), 48, 48, random.randint(70, 100), random.randint(5, 7), 10, 200))
    # every second, create an enemy instance at a random position in the room with random health and speed.

    if (pygame.time.get_ticks() - projectile_enemy_ticks) > 3000: 
        projectile_enemy_ticks = pygame.time.get_ticks()
        data["add_instances"].append(ProjectileEnemy(window, random.randint(round(-data["room"].width / 2), round(data["room"].width / 2)), random.randint(round(-data["room"].height / 2), round(data["room"].height / 2)), 48, 48, random.randint(70, 100), random.randint(3, 5), 10, 300, 1000))
    # every second, create a projectile enemy instance at a random position in the room with random health and speed.

    for i in range(len(data["all_instances"])):
        if data["all_instances"][i].remove:
            data["remove_instances"].append(i)
    # if an instance needs to be removed, its index will be appended to the remove instance list and skips next actions.

    for instance in data["all_instances"]:
        instance.tick() 
    # performs instances next action after updating.

        if instance.trail:
            data["add_instances"].append(AfterImage(window, instance.spritepath, instance.x, instance.y, instance.width, instance.height, 0, 250, 125, -1))
        # if instance trail attribute is true, create an afterimage in its position.

        if hasattr(instance, "parried"):
            #tick_pause += 30
            data["add_instances"].append(TextDisplay(window, instance.x, instance.y, 5, random.randint(60, 120), 1000, 24, "+PARRY!", (0, 0, 0)))

            if instance.type == "Projectile":
                for i in range(5):
                    data["add_instances"].append(ProjectileParticle(window, instance.x, instance.y, 12, 12, "assets/images/enemyprojectile.png", 15, random.randint(0, 360), 250))

            elif instance.type == "ChargerEnemy":
                data["add_instances"].append(Particle(window, instance.x, instance.y, 12, 12, random.randint(5, 10), random.randint(0, 360), 250))

            del instance.parried
        # creates parry text.

        if instance.type == "Player":
            data["camera"].target(instance.x - width / 2 + (mouse_x - width / 2) / 4, instance.y - height / 2 + (mouse_y - height / 2) / 4)
            # smooths camera position to mouse and player position.

            for element in data["ui"]:
                if element.name == "HealthBar":
                    element.stat = instance.health
                if element.name == "HealthText":
                    element.set_text("Health: " + str(instance.health) + "")
            # updates ui elements correlated to player stats.

            if pygame.mouse.get_pressed()[0] and (pygame.time.get_ticks() - instance.projectile_ticks) > instance.projectile_cooldown:
                instance.projectile_ticks = pygame.time.get_ticks()
                data["add_instances"].append(Projectile(window, instance.x, instance.y, 24, 24, mouse_x + data["camera"].x, mouse_y + data["camera"].y, 24, 25))
                for i in range(3):
                    data["add_instances"].append(ProjectileParticle(window, instance.x, instance.y, 12, 12, "assets/images/dot.png", 15, math.degrees(math.atan2(mouse_y + data["camera"].y - instance.y, mouse_x + data["camera"].x - instance.x)) + random.randint(-45, 45), 250))
                data["camera"].shake(7, 7)
            # if mouse is down, create a projectile instance at player position going towards mouse position, then shake the camera by 5.
            
            if pygame.mouse.get_pressed()[2] and (pygame.time.get_ticks() - instance.beam_ticks) > instance.beam_cooldown:
                instance.beam_ticks = pygame.time.get_ticks()
                data["add_instances"].append(Beam(window, instance.x, instance.y, 24, 24, mouse_x + data["camera"].x, mouse_y + data["camera"].y, 15))
                for i in range(3):
                    data["add_instances"].append(ProjectileParticle(window, instance.x, instance.y, 12, 12, "assets/images/magentadot.png", 20, math.degrees(math.atan2(mouse_y + data["camera"].y - instance.y, mouse_x + data["camera"].x - instance.x)) + random.randint(-45, 45), 150))
                data["camera"].shake(5, 5)
            # creates a beam instead.

            if pygame.key.get_pressed()[pygame.K_f] and (pygame.time.get_ticks() - instance.parry_ticks) > instance.parry_cooldown:
                instance.parry_ticks = pygame.time.get_ticks()
                data["add_instances"].append(Parry(window, instance.x, instance.y, 96, 96, "Player", 10))
                data["camera"].shake(10, 10)
            # if f is down, create a parry instance that reflects enemy projectiles and indicated attacks.

        elif (instance.type == "Enemy" or instance.type == "ProjectileEnemy" or instance.type == "ChargerEnemy") and instance.remove:
            for i in range(5):
                data["add_instances"].append(EnemyParticle(window, instance.x, instance.y, 24, 24, random.randint(5, 10), random.randint(1, 360), 3000))
        # create 5 particles on death. 

        elif instance.type == "ProjectileEnemy":
            if instance.spawn_projectile and (pygame.time.get_ticks() - instance.cooldown_ticks) > instance.projectile_cooldown:
                instance.cooldown_ticks = pygame.time.get_ticks()
                data["add_instances"].append(EnemyProjectile(window, instance.x, instance.y, 24, 24, instance.target_x, instance.target_y, 10, 10))
                for i in range(3):
                    data["add_instances"].append(ProjectileParticle(window, instance.x, instance.y, 12, 12, "assets/images/enemyprojectile.png", 15, math.degrees(math.atan2(instance.target_y - instance.y, instance.target_x - instance.x)) + random.randint(-45, 45), 250))
            # if player is in range, fire a projectile at the player.

        elif instance.type == "ChargerEnemy":
            if instance.spawn_particle:
                for i in range(3):
                    data["add_instances"].append(ParryFlash(window, instance.x, instance.y, 12, 48, random.randint(1, 360), 500, random.randint(-10, 10)))
            instance.spawn_particle = False
            # creates parry indicator particles.

        elif instance.type == "Beam":
            if instance.remove:
                data["add_instances"].append(BeamFade(window, instance.x_init, instance.y_init, instance.x, instance.y, instance.width, instance.height, 50))
            # creates a beam fading effect on its position.

    removals = 0
    for index in data["remove_instances"]:
        data["all_instances"].pop(index - removals)
        removals += 1
    data["remove_instances"] = []
    # removes instances that needs to be deleted from the instances list, then resets the remove instances list.
    
    data["camera"].random_shake()
    # assign camera shake to dedicated random integer attributes for instance rendering.

    data["room"].draw(window, (200, 200, 200), data["camera"].x + data["camera"].shake_random_x, data["camera"].y + data["camera"].shake_random_y)
    # draws the room borders.

    for instance in render_sort(data["all_instances"], data["camera"]):
        instance.render(data["camera"].x + data["camera"].shake_random_x, data["camera"].y + data["camera"].shake_random_y) 
    # renders all instances with camera attributes after ticking.

    removals = 0
    for i in range(len(data["camera"].effects)):
        if data["camera"].effects[i - removals].remove:
            data["camera"].effects.pop(i - removals)
            removals += 1
        else:
            data["camera"].effects[i - removals].render()
    # renders screen overlay effects.

    removals = 0
    for i in range(len(data["ui"])):
        if data["ui"][i - removals].remove:
            data["ui"].pop(i - removals)
            removals += 1
        else:
            data["ui"][i - removals].render()
    # removes ui elements that need to be removed; else render the ui element.

    pygame.display.flip()
    # updates the display after rendering all instances.

    clock.tick(tickrate)
    # updates main loop at set tickrate.

    while tick_pause > 0:
        clock.tick(tickrate)
        tick_pause -= 1
    # pauses main loop for tick pause duration.
# end of main loop.

_start_time = time.perf_counter()
print("\nSaving...")
save_data = [
    ["instance", "x", "y"]
]
# prepares program data for save after quitting, starts with column labels.

for instance in data["all_instances"]:
    save_data.append([instance.type, int(instance.x), int(instance.y)])
# adds player data to the save.

with open(save_path, mode="w", newline="") as save:
    writer = csv.writer(save)
    writer.writerows(save_data)
# writes completed data to the save. (currently just acts as placeholder)

print("Saved. (" + str(time.perf_counter() - _start_time) + " seconds)" + "\n" * 2 + "Program Successfully Ended\n")
# prints successful save with elapsed time.

sys.exit()