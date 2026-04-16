import pygame
import sys
import os

from scripts.player import Player
from scripts.enemy import Enemy
from scripts.projectile import Projectile
# imports necessary modules and classes.

pygame.init()
# initializes all imported pygame modules.

width, height = 800, 600
window = pygame.display.set_mode([width, height])
# creates a window with the specified width and height.

running = True
clock = pygame.time.Clock()
tickrate = 60
camera_x = -width / 2
camera_y = -height / 2
# initializes variables for the main loop, including a clock for controlling frame rate and placeholders for camera position.

all_instances = [Player(window, width / 2, height / 2, 15, 15, 5), 
                 Enemy(window, (width / 3) * 2, height / 2, 15, 15, 3)]
all_instances_remove = []

while running:

    if pygame.key.get_pressed()[pygame.K_DELETE]:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # checks for quit events and if the delete key is pressed to end the program.

    window.fill((255, 255, 255))
    # fills the window with white color to clear previous frames.

    mouse_x, mouse_y = pygame.mouse.get_pos()
    # gets the current position of the mouse cursor.

    for instance in all_instances:
        instance.update(all_instances) 
        # updates each instance.

        if instance.type == "Player" and pygame.mouse.get_pressed()[0]:
            all_instances.append(Projectile(window, instance.x, instance.y, 5, 5, (mouse_x + camera_x, mouse_y + camera_y), 7, 25))
        # if mouse is down, create a projectile instance at player position going towards mouse position.

    for instance in all_instances:
        instance.tick() 
        # performs instances next action after updating.

        if instance.delete:
            all_instances_remove.append(all_instances.index(instance))
            continue
        # if an instance needs to be deleted, its index will be appended to the remove instance list and skips next actions.

        if instance.type == "Player":
            camera_x = instance.x - width / 2
            camera_y = instance.y - height / 2
        # centers camera position to players position.
    
    _removals = 0
    for index in all_instances_remove:
        try: 
            all_instances.pop(index - _removals)
            _removals += 1

        except IndexError:
            print("FATAL ERROR: IndexError when attempting to remove an instance.")
            break
        # fail-safe mechanism in case index is out of range (happens way too often. x_x)

    all_instances_remove = []
    # removes instances that needs to be deleted from the instances list.

    for instance in all_instances:
        instance.render(camera_x, camera_y) 
    # TODO: add priority for instance rendering (ex: player always renders over all other instances)
    # renders all instances after running.

    pygame.display.flip()
    # updates the display after rendering all instances.

    clock.tick(tickrate)

print("\nProgram Successfully Ended\n")

sys.exit()