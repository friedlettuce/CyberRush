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
        self.frame_counter = 0

        self.left_frames = []
        self.right_frames = []
        self.frame = None
        self.frame_rect = None

        self.hitbox_x = 0
        self.hitbox_y = 0
        self.hitbox_color = (255, 0, 0)

        # Range for how wide enemy can see (range will be 2x this value)
        self.eye_sight = 0

        self.projectiles = []
        self.projectile_speed = None
        self.projectile_num = None

        #flag for if enemy moves
        #default false
        #should be set to true for each enemy type that moves
        self.moving = False

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
                self.frame_counter = 0
                
        # If Velocity < 0, Enemy Is Moving To The Left
        elif self.vel_x < 0:
            if self.x > self.path_x[0] - self.vel_x:
                self.facing_right = False
                self.x = self.x + self.vel_x
            else:
                self.facing_right = True
                self.vel_x *= -1
                self.x = self.x + self.vel_x
                self.frame_counter = 0
    
    # Function For An Enemy To Move Side To Side On The Y Axis
    def update_y(self):
        # If Velocity > 0, Enemy Is Moving Down
        if self.vel_y > 0:
            if self.y < self.path_y[1] + self.vel_y:
                self.y += self.vel_y
            else:
                self.vel_y *= -1
                self.y += self.vel_y
                self.frame_counter = 0
                
        # If Velocity < 0, Enemy Is Moving Up
        elif self.vel_y < 0:
            if self.y > self.path_y[0] - self.vel_y:
                self.y += self.vel_y
            else:
                self.vel_y *= -1
                self.y += self.vel_y
                self.frame_counter = 0

    def update_hitbox(self):
        # Place holder for enemy object hitbox
        pass

    def update(self):

        if self.moving_x:
            self.update_x()
        if self.moving_y:
            self.update_y()

        if self.frame_counter + 1 == 60:
            self.frame_counter = 0

        # Changes frames as enemy moves left/right
        if self.vel_x < 0 and self.moving_x or not self.facing_right:
            self.frame = self.left_frames[self.frame_counter // 30]
        elif (self.vel_x >= 0 and self.moving_x) or self.facing_right:
            self.frame = self.right_frames[self.frame_counter // 30]

        # Sets hitbox vertical and horizontal start/width/height
        self.update_hitbox()

        for projectile in self.projectiles:
            if projectile.move() == 0:
                self.projectiles.remove(projectile)

    def add_projectile(self, dir_x=0, dir_y=0):
        # Sets x travel direction based on enemy facing direction
        if self.facing_right == 1:
            dir_x = self.facing_right
        else:
            dir_x = -1

        # Adds a projectile if it hasn't shot to many yet
        if len(self.projectiles) < self.projectile_num:
            self.projectiles.append(Projectile(self.screen,
                self.frame_rect.centerx + self.x, self.y + int(self.frame_rect.height * .2), 10,
                    5, dir_x, dir_y, self.projectile_speed))

    def range_y(self, y):
        y = int(y)
        # Checks if y is in a 40 pixel range of self
        return self.y in range(y - self.eye_sight, y + self.eye_sight)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def check_collision(self, obj_rect):
        if self.get_rect().colliderect(obj_rect):
            return True

        return False

    def move_by_amount(self, x, y):
        #moves mob by specified x and y number of pixels
        #used for collision testing
        self.x += x
        self.y += y

    def blitme(self):

        #self.update()
        self.screen.blit(self.frame, (self.x, self.y, self.width, self.height))

        #Draws vert/horiz hitboxes, hardcoded color for now
        #pygame.draw.rect(self.screen, self.hitbox_color, self.hitbox_x, 2)
        #pygame.draw.rect(self.screen, self.hitbox_color, self.hitbox_y, 2)

        for projectile in self.projectiles:
            projectile.blitme()

        self.frame_counter += 1


class HoveringEnemy(Enemy):
    # Stores frames

    def __init__(self, screen, game_settings, x, y, width, height, end_x=0, end_y=0):
        super().__init__(screen, x, y, width, height, end_x, end_y)

        #this enemy moves
        self.moving = True

        self.left_frames = [pygame.transform.scale(pygame.image.load(game_settings.rhl1_path), game_settings.hov_size),
                         pygame.transform.scale(pygame.image.load(game_settings.rhl2_path), game_settings.hov_size)]
        self.right_frames = [pygame.transform.scale(pygame.image.load(game_settings.rhr1_path), game_settings.hov_size),
                          pygame.transform.scale(pygame.image.load(game_settings.rhr2_path), game_settings.hov_size)]

        self.frame = self.right_frames[0]
        self.frame_rect = self.right_frames[0].get_rect()
        self.projectile_speed = game_settings.hov_proj_speed
        self.projectile_num = game_settings.hov_proj_num

        # If the enemy moves along a path, sets velocity not to 0
        if self.moving_x:
            self.vel_x = game_settings.hovering_enemy_vel
        if self.moving_y:
            self.vel_y = game_settings.hovering_enemy_vel

        self.hitbox_x = (self.x + 50, self.y + 25, 45, 110)
        self.hitbox_y = (self.x + 40, self.y + 25, 80, 35)
        self.hitbox_color = (255, 0, 0)
        self.eye_sight = 20

    def update_hitbox(self):
        self.hitbox_x = (self.x + 50, self.y + 25, 45, 110)
        self.hitbox_y = (self.x + 40, self.y + 25, 80, 35)


class Projectile(object):

    def __init__(self, screen, x, y, width, height, dir_x, dir_y, speed):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.speed_x = dir_x * speed
        self.speed_y = dir_y * speed

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Activates removal if off screen
        if (self.x > self.screen_rect.width or self.x < 0) or (
                self.y > self.screen_rect.height or self.y < 0):
            return 0    # Pop self
        return 1

    def blitme(self):
        pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y, self.width, self.height))
