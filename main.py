import pygame
import random
import sys

from scripts.player import Player
from scripts.enemy import Enemy
from scripts.projectile import Projectile, Beam
from scripts.render_sort import render_sort

pygame.init()

width, height = 800, 600
window = pygame.display.set_mode([width, height])
# creates a window with the specified width and height.

running = True
clock = pygame.time.Clock()
tickrate = 60
camera_x = -width / 2
camera_y = -height / 2
camera_smoothing = 0.1
camera_x_shake = 0
camera_y_shake = 0
shake_decay = 0.
room_width = width * 2
room_height = height * 2

_camera_x_shake = 0
_camera_y_shake = 0
_removals = 0
# initializes variables for the main loop, including a clock for controlling frame rate and placeholders for camera position.

all_instances = [Player(window, 0, 0, 15, 15, room_width, room_height, 100, 5), 
                 Enemy(window, (room_width / 4), 0, 15, 15, room_width, room_height, 100, 3)]
remove_instances = []
add_instances = []
# initialize instance lists.

while running:
# main loop.

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # checks for quit events and if the escape key is pressed to end the program.

    window.fill((200, 200, 200))
    # fills the window with white color to clear previous frames.

    mouse_x, mouse_y = pygame.mouse.get_pos()
    # gets the current position of the mouse cursor.

    for instance in add_instances:
        all_instances.append(instance)
    add_instances = []
    # adds queued instances to the instance list, then clears the add instances list.

    for instance in all_instances:
        instance.update(all_instances) 
    # updates each instance before doing anything.

        if instance.type == "Player":
            if pygame.mouse.get_pressed()[0]:
                add_instances.append(Projectile(window, instance.x, instance.y, 5, 5, room_width, room_height, (mouse_x + camera_x, mouse_y + camera_y), 15, 25))
                camera_x_shake += 5
                camera_y_shake += 5
            # if mouse is down, create a projectile instance at player position going towards mouse position.
            
            if pygame.mouse.get_pressed()[2]:
                add_instances.append(Beam(window, instance.x, instance.y, 5, 5, room_width, room_height, (mouse_x + camera_x, mouse_y + camera_y), 15, 25))
            # creates a beam instead.
    
    for i in range(len(all_instances)):
        if all_instances[i].remove:
            remove_instances.append(i)
    # if an instance needs to be removed, its index will be appended to the remove instance list and skips next actions.

    camera_x_shake *= shake_decay
    camera_y_shake *= shake_decay
    # camera shake decay.

    for instance in all_instances:
        instance.tick() 
    # performs instances next action after updating.

        if instance.type == "Player":
            target_x = instance.x - width / 2   
            target_y = instance.y - height / 2
            camera_x += (target_x - camera_x) * camera_smoothing
            camera_y += (target_y - camera_y) * camera_smoothing
        # smooths camera position to players position.

    _removals = 0
    for index in remove_instances:
        all_instances.pop(index - _removals)
        _removals += 1
    remove_instances = []
    # removes instances that needs to be deleted from the instances list, then resets the remove instances list.
    
    _camera_x_shake = random.randint(-round(camera_x_shake), round(camera_x_shake))
    _camera_y_shake = random.randint(-round(camera_y_shake), round(camera_y_shake))
    # manage random camera shake integers by assigning it to a variable so all instances are offsetted equally.
    pygame.draw.circle(window, (255, 255, 255), (-camera_x, -camera_y), 10)
    for instance in render_sort(all_instances):
        instance.render(camera_x + _camera_x_shake, camera_y + _camera_y_shake) 
    # renders all instances with camera variables after running.

    pygame.display.flip()
    # updates the display after rendering all instances.

    clock.tick(tickrate)
    # updates main loop at set tickrate.

print("\nProgram Successfully Ended\n")

sys.exit()