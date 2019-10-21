import pygame


# Generic Enemy Class For Enemies To Utilize
class Enemy(object):
    # Enemy class handles directional movement, hitbox, and frames
    
    def __init__(self, screen, x, y, width, height, end_x, end_y):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.vel_x = 0
        self.vel_y = 0

        self.end_x = end_x
        if end_x <= 0:
            self.end_x = self.x

        self.end_y = end_y
        if end_y <= 0:
            self.end_y = self.y

        # Flags for direction of / movement
        self.moving_x = (self.x != self.end_x)
        self.moving_y = (self.y != self.end_y)
        self.facing_right = False

        self.path_x = [self.x, self.end_x]
        self.path_y = [self.y, self.end_y]
        self.movement = 0

        self.left_frames = []
        self.right_frames = []
        self.frame = None

        self.hitbox = 0
        self.hitbox2 = 0

        self.projectiles = []
        self.projectile_speed = None

    # Function For An Enemy To Move Side To Side On The X Axis
    def update_x(self):
        # If Velocity > 0, Enemy Is Moving To The Right
        if self.vel_x > 0:
            if self.x < self.path_x[1] + self.vel_x:
                self.facing_right = True
                self.x = self.x + self.vel_x
            else:
                self.facing_right = False
                self.vel_x *= -1
                self.x = self.x + self.vel_x
                self.movement = 0
                
        # If Velocity < 0, Enemy Is Moving To The Left
        elif self.vel_x < 0:
            if self.x > self.path_x[0] - self.vel_x:
                self.facing_right = False
                self.x = self.x + self.vel_x
            else:
                self.facing_right = True
                self.vel_x *= -1
                self.x = self.x + self.vel_x
                self.movement = 0
    
    # Function For An Enemy To Move Side To Side On The Y Axis
    def update_y(self):
        # If Velocity > 0, Enemy Is Moving Down
        if self.vel_y > 0:
            if self.y < self.path_y[1] + self.vel_y:
                self.y += self.vel_y
            else:
                self.vel_y *= -1
                self.y += self.vel_y
                self.movement = 0
                
        # If Velocity < 0, Enemy Is Moving Up
        elif self.vel_y < 0:
            if self.y > self.path_y[0] - self.vel_y:
                self.y += self.vel_y
            else:
                self.vel_y *= -1
                self.y += self.vel_y
                self.movement = 0

    def update(self):
        if self.moving_x:
            self.update_x()
        if self.moving_y:
            self.update_y()

        if self.movement + 1 == 60:
            self.movement = 0

        # Changes frames as enemy moves left/right
        if self.vel_x < 0 and self.moving_x or not self.facing_right:
            self.frame = self.left_frames[self.movement // 30]
        elif (self.vel_x >= 0 and self.moving_x) or self.facing_right:
            self.frame = self.right_frames[self.movement // 30]

        self.hitbox = (self.x + 50, self.y + 25, 45, 110)
        self.hitbox2 = (self.x + 40, self.y + 25, 80, 35)

        for projectile in self.projectiles:
            if projectile.move() == 0:
                self.projectiles.remove(projectile)

    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox2, 2)

        if not self.vel_y > self.path_y[0] - self.vel_y:
            pass
            # Projectile(self.x, self.y + 40, 25, 25, -1, screen)
        elif not self.vel_y < self.path_y[1] + self.vel_y:
            pass
            # Projectile(self.x, self.y + 20, 25, 25, -1, screen)

    def blitme(self):

        self.update()
        self.screen.blit(self.frame, (self.x, self.y))
        # self.draw_hitbox(screen)

        for projectile in self.projectiles:
            projectile.blitme()

        self.movement += 1


class HoveringEnemy(Enemy):
    # Stores frames

    def __init__(self, screen, game_settings, x, y, width, height, end_x=0, end_y=0):
        super().__init__(screen, x, y, width, height, end_x, end_y)

        self.left_frames = [pygame.transform.scale(pygame.image.load(game_settings.rhl1_path), game_settings.hov_size),
                         pygame.transform.scale(pygame.image.load(game_settings.rhl2_path), game_settings.hov_size)]
        self.right_frames = [pygame.transform.scale(pygame.image.load(game_settings.rhr1_path), game_settings.hov_size),
                          pygame.transform.scale(pygame.image.load(game_settings.rhr2_path), game_settings.hov_size)]

        self.frame = self.right_frames[0]
        self.projectile_speed = game_settings.hov_proj_speed

        # If the enemy moves along a path, sets velocity not to 0
        if self.moving_x:
            self.vel_x = game_settings.hovering_enemy_vel
        if self.moving_y:
            self.vel_y = game_settings.hovering_enemy_vel


class Projectile(object):

    def __init__(self, screen, x, y, width, height, dir_x, dir_y, speed):

        self.screen = screen

        self.x = self.start_x = x
        self.y = self.start_y = y
        self.width = width
        self.height = height

        self.dir_x = dir_x
        self.dir_y = dir_y
        self.speed = speed

    def move(self):
        self.x += self.speed * self.dir_x
        self.y += self.speed * self.dir_y

        if (self.x < self.start_x - 250) or (self.y < self.start_y - 250):
            return 0    # Pop self

    def blitme(self):
        pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y, self.width, self.height))
