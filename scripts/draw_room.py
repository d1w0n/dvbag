import pygame

pygame.init()

def draw_room(window, room_width, room_height, camera_x, camera_y):
    pygame.draw.line(window, (255, 255, 255), (-room_width / 2 - camera_x, -room_height / 2 - camera_y), (room_width / 2 - camera_x, -room_height / 2 - camera_y), 5)
    # top border.

    pygame.draw.line(window, (255, 255, 255), (room_width / 2 - camera_x, -room_height / 2 - camera_y), (room_width / 2 - camera_x, room_height / 2 - camera_y), 5)
    # right border.

    pygame.draw.line(window, (255, 255, 255), (room_width / 2 - camera_x, room_height / 2 - camera_y), (-room_width / 2 - camera_x, room_height / 2 - camera_y), 5)
    # bottom border.

    pygame.draw.line(window, (255, 255, 255), (-room_width / 2 - camera_x, room_height / 2 - camera_y), (-room_width / 2 - camera_x, -room_height / 2 - camera_y), 5)
    # left border.