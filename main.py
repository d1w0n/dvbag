import pygame
import random
import sys

from scripts.room import Room
from scripts.camera import Camera
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
ticks = 0

_removals = 0
# initializes variables for the main loop, including a clock for controlling frame rate and placeholders for camera position.

room = Room(width * 2, height * 2)
camera = Camera(-width / 2, -height / 2, 0.1, 0.8)
# initializes variables from camera and room classes.

all_instances = [Player(window, 0, 0, 15, 15, 100, 5), 
                 Enemy(window, (room.width / 4), 0, 15, 15, 100, 3, 10)]
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

    window.fill((255, 255, 255))
    # fills the window with white color to clear previous frames.

    mouse_x, mouse_y = pygame.mouse.get_pos()
    # gets the current position of the mouse cursor.

    for instance in add_instances:
        all_instances.append(instance)
    add_instances = []
    # adds queued instances to the instance list, then clears the add instances list.

    for instance in all_instances:
        instance.update(all_instances, room, camera)
    # updates each instance before doing anything.

        if instance.type == "Player":
            if pygame.mouse.get_pressed()[0] and (pygame.time.get_ticks() - instance.cooldown_ticks) > instance.projectile_cooldown:
                instance.cooldown_ticks = pygame.time.get_ticks()
                add_instances.append(Projectile(window, instance.x, instance.y, 5, 5, mouse_x + camera.x, mouse_y + camera.y, 15, 25))
                camera.shake(7, 7)
            # if mouse is down, create a projectile instance at player position going towards mouse position, then shake the camera by 5.
            
            if pygame.mouse.get_pressed()[2]:
                add_instances.append(Beam(window, instance.x, instance.y, 5, 5, (mouse_x + camera.x, mouse_y + camera.y), 15, 25))
            # creates a beam instead.

    if (pygame.time.get_ticks() - ticks) > 1000: 
        ticks = pygame.time.get_ticks()
        add_instances.append(Enemy(window, random.randint(round(-room.width / 2), round(room.width / 2)), random.randint(round(-room.height / 2), round(room.height / 2)), 15, 15, random.randint(70, 100), random.randint(3, 5), 10))
    # every 3 seconds, create an enemy instance at a random position in the room with random health and speed.
    # currently a placeholder.
    
    for i in range(len(all_instances)):
        if all_instances[i].remove:
            remove_instances.append(i)
    # if an instance needs to be removed, its index will be appended to the remove instance list and skips next actions.

    camera.shake_decay()
    # multiplies camera shake attributes by its decay.

    for instance in all_instances:
        instance.tick() 
    # performs instances next action after updating.

        if instance.type == "Player":
            camera.target(instance.x - width / 2 + (mouse_x - width / 2) / 5, instance.y - height / 2 + (mouse_y - height / 2) / 5)
        # smooths camera position to mouse and player position.

    _removals = 0
    for index in remove_instances:
        all_instances.pop(index - _removals)
        _removals += 1
    remove_instances = []
    # removes instances that needs to be deleted from the instances list, then resets the remove instances list.
    
    camera.random_shake()
    # assign camera shake to dedicated random integer attributes for instance rendering.
    
    pygame.draw.circle(window, (200, 200, 200), (-camera.x + camera.shake_random_x, -camera.y + camera.shake_random_y), 3) 
    # ORIGIN PLACEHOLDER

    room.draw(window, (200, 200, 200), camera.x + camera.shake_random_x, camera.y + camera.shake_random_y)
    # draws the room borders.

    for instance in render_sort(all_instances):
        instance.render(camera.x + camera.shake_random_x, camera.y + camera.shake_random_y) 
    # renders all instances with camera attributes after ticking.

    pygame.display.flip()
    # updates the display after rendering all instances.

    clock.tick(tickrate)
    # updates main loop at set tickrate.

print("\nProgram Successfully Ended\n")

sys.exit()