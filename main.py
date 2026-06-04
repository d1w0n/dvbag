import time
_start_time = time.perf_counter()
print("\nLoading...")

import random
import csv
import sys
import os
try:
    import pygame
except ModuleNotFoundError:
    print("\nPygame is not installed. Please install Pygame! Instructions below.\n \
          1. Open the terminal\n \
          2. Enter this command: \'pip install pygame\'\n \
          3. Retry this program!" + "\n" * 2 + "Program Successfully Ended\n")
    sys.exit()

import config

"""
instance management is no longer in main; it just handles the main game loops now.
for instance management, check scripts/instance_managers.py
"""
from scripts.room import Room
from scripts.camera import Camera
from scripts.instance_managers import InstanceLists, UIList

pygame.init()

width, height = 800, 600
window = pygame.display.set_mode([width, height])
# creates a window with the specified width and height.

running = True
clock = pygame.time.Clock()
tickrate = 60
removals = 0
tick_pause = 0
# variable initialization.

data = {
    "ui": UIList()
}
# initializes menu data.

data["ui"].add_Text("Title", window, 0, 0, 96, "this is technically a menu", (0, 0, 0))
# initialize menu ui elements.

print("Loaded. (" + str(time.perf_counter() - _start_time) + " seconds)")

while not config.MENU_SKIP and running:
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((255, 255, 255))

    if pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_SPACE]:
        break

    data["ui"].ui_render()
    # removes ui elements that need to be removed.

    pygame.display.flip()

    clock.tick(tickrate)
# menu loop.

_start_time = time.perf_counter()
print("\nLoading save...")

enemy_ticks = 0
projectile_enemy_ticks = 0

_save_has_player = False
score = 0
tick_pause = 0
# main gameplay loop variables.

data = {
    "window": window,
    "width": width,
    "height": height,
    "room": Room(width * 2, height * 2),
    "camera": Camera(window, -width / 2, -height / 2, width, height, 0.1, 0.8),
    "instances": InstanceLists(),
    "ui": UIList(),
    "mouse_x": pygame.mouse.get_pos()[0],
    "mouse_y": pygame.mouse.get_pos()[1],
    "score": 0,
    "tick_pause": 0
}
# initialize main loop data.

data["ui"].add_Bar("HealthBar", window, 0, 0, width / 2, 50, (0, 255, 0))
data["ui"].add_Text("HealthText", window, 10, 60, 36, "", (0, 255, 0))
data["ui"].add_Text("ScoreText", window, 10, height - 50, 48, "Score: " + str(data["score"]), (0, 0, 0))
# initialize main loop ui elements.

save_path = os.path.join(config.BASE_DIR, "saves", "save.csv")
# get save file location.

if os.path.exists(save_path):
    try:
        with open(save_path, "r") as save:
            csv_reader = csv.DictReader(save)
            for row in csv_reader:
                if row["instance"] == "Player":
                    _save_has_player = True
                    data["instances"].add_Player(window, float(row["x"]), float(row["y"]), 48, 48, 100, 5)
                    data["camera"].x = float(row["x"]) - width / 2
                    data["camera"].y = float(row["y"]) - height / 2
                # sets player position to saved position.

                elif row["instance"] == "Enemy":
                    data["instances"].add_Enemy(window, float(row["x"]), float(row["y"]), 48, 48, 100, 3, 10)

                elif row["instance"] == "ProjectileEnemy":
                    data["instances"].add_ProjectileEnemy(window, float(row["x"]), float(row["y"]), 48, 48, random.randint(70, 100), random.randint(3, 5), 10, 300, 1000)

                elif row["instance"] == "ChargerEnemy":
                    data["instances"].add_ChargerEnemy(window, float(row["x"]), float(row["y"]), 48, 48, random.randint(70, 100), random.randint(5, 7), 10, 200)

    except:
        print("Save file data is corrupted! Creating a new save file...")
# if there is a save file, load the instances with their positions from there.

else:
    print("Save file not found. Creating a new save file...")
    open(save_path, mode="w", newline="")
# creates a new save file if the file is not found (happens when cloning the github repository.)

if not _save_has_player:
    data["instances"] = InstanceLists()
    data["instances"].add_Player(window, 0, 0, 48, 48, 100, 5)
    data["instances"].add_Enemy(window, data["room"].width / 4, 0, 48, 48, 100, 3, 10)
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

    data["mouse_x"], data["mouse_y"] = pygame.mouse.get_pos()
    # gets the current position of the mouse cursor.

    data["camera"].shake_decay()
    # multiplies camera shake attributes by its decay.

    data["instances"].append_queued()
    # adds queued instances from the add_instances list to the all_instances list, then clears the add_instances list.
    
    for instance in data["instances"].all_instances:
        if instance.can_pre_update:
            instance.pre_update(data)
    # runs pre-update for instances that have that priority.

    for instance in data["instances"].all_instances:
        instance.update(data)
    # updates each instance before doing anything.

    if (pygame.time.get_ticks() - enemy_ticks) > 3000: 
        enemy_ticks = pygame.time.get_ticks()
        data["instances"].add_ChargerEnemy(window, random.randint(round(-data["room"].width / 2), round(data["room"].width / 2)), random.randint(round(-data["room"].height / 2), round(data["room"].height / 2)), 48, 48, random.randint(70, 100), random.randint(5, 7), 10, 200)
    # every second, create an enemy instance at a random position in the room with random health and speed.

    if (pygame.time.get_ticks() - projectile_enemy_ticks) > 3000: 
        projectile_enemy_ticks = pygame.time.get_ticks()
        data["instances"].add_ProjectileEnemy(window, random.randint(round(-data["room"].width / 2), round(data["room"].width / 2)), random.randint(round(-data["room"].height / 2), round(data["room"].height / 2)), 48, 48, random.randint(70, 100), random.randint(3, 5), 10, 300, 1000)
    # every second, create a projectile enemy instance at a random position in the room with random health and speed.

    data["instances"].queue_removals()
    # if an instance needs to be removed, its index will be appended to the remove instance list.

    for instance in data["instances"].all_instances:
        instance.tick(data) 
    # performs instances next action after updating.

    data["instances"].remove_queued()
    # removes instances that needs to be deleted from the instances list, then resets the remove instances list.
    
    data["camera"].random_shake()
    # assign camera shake to dedicated random integer attributes for instance rendering.

    data["room"].draw(window, (200, 200, 200), data["camera"])
    # draws the room borders.

    for instance in data["instances"].render_sort(data["camera"]):
        instance.render(data["camera"]) 
    # renders all instances with camera attributes after ticking.

    data["ui"].effects_render()
    # renders screen overlay effects.

    data["ui"].ui_render()
    # removes ui elements that need to be removed; else render the ui element.

    pygame.display.flip()
    # updates the display after rendering all instances.

    clock.tick(tickrate)
    # updates main loop at set tickrate.

    while data["tick_pause"] > 0:
        clock.tick(tickrate)
        data["tick_pause"] -= 1
    # pauses main loop for tick pause duration.
# end of main loop.

_start_time = time.perf_counter()
print("\nSaving...")
save_data = [
    ["instance", "x", "y"]
]
# prepares program data for save after quitting, starts with column labels.

for instance in data["instances"].all_instances:
    save_data.append([instance.type, int(instance.x), int(instance.y)])
# adds player data to the save.

with open(save_path, mode="w", newline="") as save:
    writer = csv.writer(save)
    writer.writerows(save_data)
# writes completed data to the save. (currently just acts as placeholder)

print("Saved. (" + str(time.perf_counter() - _start_time) + " seconds)" + "\n" * 2 + "Program Successfully Ended\n")
# prints successful save with elapsed time.

sys.exit()