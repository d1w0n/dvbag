from scripts.instance import Instance
import pygame
import math

pygame.init()

class Projectile(Instance):
    def __init__(self, window, x, y, width, height, target_x, target_y, speed: int, damage: int, add_x_velocity = 0, add_y_velocity = 0):
        super().__init__("Projectile", "assets/images/placeholder.png", window, x, y, width, height)
        self.damage = damage
        self.speed = speed
        self.velocity_x, self.velocity_y = self.get_velocity(target_x - self.x, target_y - self.y, self.speed)

    def update(self, instance_list, room, camera):
        self._room = room
        for instance in instance_list:
            if instance.type == "Enemy" or instance.type == "ProjectileEnemy" or instance.type == "ChargerEnemy":
                if self.get_collision(instance):
                    self.remove = True
                # if colliding with an enemy, remove itself.

        if self.get_room_collision_x(room) or self.get_room_collision_y(room):
            self.remove = True
        # if colliding with room bounds, remove itself.

    def tick(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        # change x and y by velocities.

    def render(self, camera_x, camera_y):
        self._window.blit(self._sprite, (self.x - self.width / 2 - camera_x, self.y - self.height / 2 - camera_y))



class Parry(Instance):
    def __init__(self, window, x, y, width, height, target_instance, damage):
        super().__init__("Parry", "assets/images/placeholder.png", window, x, y, width, height)
        self._target_instance = target_instance
        self.damage = damage
        self.start_ticks = pygame.time.get_ticks()
        self._duration = 250
        self._has_target = False

    def update(self, instance_list, room, camera):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self._has_target = False
        for instance in instance_list:
            if instance.type == self._target_instance:
                self._mouse_dx = mouse_x + camera.x - instance.x
                self._mouse_dy = mouse_y + camera.y - instance.y
                self._target_x, self._target_y = self.get_velocity(self._mouse_dx, self._mouse_dy, instance.width / 2)
                self._target_x += instance.x
                self._target_y += instance.y
                self._has_target = True

            elif instance.type == "EnemyProjectile" or (instance.type == "Projectile" and instance.parried) or instance.type == "ChargerEnemy":
                if self.get_collision(instance):
                    self.remove = True
        
        if not self._has_target:
            self.remove = True
                
        if (pygame.time.get_ticks() - self.start_ticks) > self._duration:
            self.remove = True

    def tick(self):
        self.x = self._target_x
        self.y = self._target_y
        self._angle = -math.degrees(math.atan2(self._mouse_dy, self._mouse_dx))

    def render(self, camera_x, camera_y):
        _rotated = pygame.transform.rotate(self._sprite, self._angle)
        _rect = _rotated.get_rect(center=(self.x - camera_x, self.y - camera_y))
        self._window.blit(_rotated, _rect.topleft)





class EnemyProjectile(Projectile):
    def __init__(self, window, x, y, width, height, target_x, target_y, speed: int, damage: int, add_x_velocity = 0, add_y_velocity = 0):
        super().__init__(window, x, y, width, height, target_x, target_y, speed, damage)
        self.type = "EnemyProjectile"
        self.parry_text = False
        self.trail = True
        self.set_sprite("assets/images/enemyprojectile.png")

    def update(self, instance_list, room, camera):
        if self.type == "EnemyProjectile":
            self._room = room
            for instance in instance_list:
                if instance.type == "Player":
                    if self.get_collision(instance):
                        self.remove = True
                    # if colliding with an enemy, remove itself.

                elif instance.type == "Parry":
                    if self.get_collision(instance):
                        self.type = "Projectile"
                        self.parried = True
                        self.damage = 100
                        self.add_score += 25
                        camera.shake(20, 20)
                        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                        self.velocity_x, self.velocity_y = self.get_velocity((self.mouse_x + camera.x) - self.x, (self.mouse_y + camera.y) - self.y, self.speed * 2)
        
        elif self.type == "Projectile":
            super().update(instance_list, room, camera)

        if self.get_room_collision_x(room) or self.get_room_collision_y(room):
            self.remove = True
        # if colliding with room bounds, remove itself.





class Beam(Instance):
    def __init__(self, window, x, y, width, height, target_x, target_y, damage: int):
        super().__init__("Beam", "assets/images/placeholder.png", window, x, y, width, height)
        self.speed = height if height <= width else width
        self.damage = damage
        self._dx = target_x - self.x
        self._dy = target_y - self.y
        self.velocity_x, self.velocity_y = self.get_velocity(self._dx, self._dy, self.speed)
        self.x_init = self.x
        self.y_init = self.y
        self._collision = False
        self.can_pre_update = True

    def pre_update(self, instance_list, room, camera):
        self._room = room
        if self._collision:
            self.remove = True
            pass
        
        for instance in instance_list:
            if instance.type == "Enemy" or instance.type == "ProjectileEnemy" or instance.type == "ChargerEnemy":
                if self.get_collision(instance):
                    self._collision = True

            if self.get_room_collision_x(room) or self.get_room_collision_y(room):
                self._collision = True

        if not self._collision:
            while not self._collision:
                for instance in instance_list:
                    if instance.type == "Enemy" or instance.type == "ProjectileEnemy" or instance.type == "ChargerEnemy":
                        if self.get_collision(instance):
                            self._collision = True
                        # if colliding with an enemy, remove itself.

                if self.get_room_collision_x(room) or self.get_room_collision_y(room):
                    self._collision = True
                # if colliding with room bounds, remove itself.

                self.x += self.velocity_x
                self.y += self.velocity_y

            self.velocity_x, self.velocity_y = self.get_velocity(self._dx, self._dy, 1)

            while self._collision:
                self.x -= self.velocity_x
                self.y -= self.velocity_y
                self._collision = False

                for instance in instance_list:
                    if instance.type == "Enemy" or instance.type == "ProjectileEnemy" or instance.type == "ChargerEnemy":
                        if self.get_collision(instance):
                            self._collision = True

                if self.get_room_collision_x(room) or self.get_room_collision_y(room):
                    self._collision = True

            self.x += self.velocity_x
            self.y += self.velocity_y
            self._collision = True

    def update(self, instance_list, room, camera):
        pass

    def tick(self):
        pass

    def render(self, camera_x, camera_y):
        pygame.draw.line(self._window, (255, 0, 255), (self.x_init - camera_x, self.y_init - camera_y), (self.x - camera_x, self.y - camera_y), self.width)
        pygame.draw.circle(self._window, (255, 0, 255), (self.x - camera_x, self.y - camera_y), self.width / 2)