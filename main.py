import pygame
import sys
#import os

from scripts.player import Player
from scripts.enemy import Enemy

pygame.init()

width, height = 800, 600
window = pygame.display.set_mode([width, height])

running = True
clock = pygame.time.Clock()
ticks = 0

all_instances = [Player(window, width / 2, height / 2, 5), 
                 Enemy(window, (width / 3) * 2, height / 2)]

while running:

    if pygame.key.get_pressed()[pygame.K_DELETE]:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((255, 255, 255))

    for instance in all_instances:
        instance.update(all_instances)

    for instance in all_instances:
        instance.tick()
        if instance.type == "Player":
            camera_x = instance.x - width / 2
            camera_y = instance.y - height / 2

    for instance in all_instances:
        instance.render(camera_x, camera_y)
    
    pygame.display.flip()

    clock.tick(60)

print("\nProgram Successfully Ended\n")
sys.exit()