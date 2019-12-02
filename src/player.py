from enum import Enum

import pygame


class Player:

    def __init__(self, screen, game_settings, x, y):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.size = game_settings.player_size
        self.width = self.size[0]
        self.height = self.size[1]

        # Loads frames for player
        self.idle_f = Frames(self.size)
        self.walking_f = Frames(self.size)
        self.jumping_f = Frames(self.size)
        self.shooting_f = Frames(self.size)

        self.proj_f = Frames(game_settings.player_frames['projectile']['size'])

        self.load_frames(game_settings.player_frames)

        # Stores projectiles for the player
        self.projectiles = []
        self.proj_max = 1
        
        # Initial Player Starting Point
        self.x = x
        self.y = y
        self.ground = None
        self.vel_x = game_settings.player_speed
        self.vel_y = 0
        self.vel_jump = game_settings.player_jump
        
        # Flags for if player is moving/facing left/right, idle, walking_f
        self.facing_right = True
        self.moving_left = False
        self.moving_right = False
        self.jumping = False
        self.shooting = False

        # Inits frame
        self.frame_count = 0
        self.frame_wait = 0
        self.fps_div = game_settings.player_counter_divisor
        self.fps_max = game_settings.player_counter_max

        self.current_frame = self.idle_f.frame(self.frame_count, self.facing_right)
        self.max_fc = self.idle_f.fc

        # Player health
        self.health = game_settings.player_health

        # Sounds
        self.player_jump_sound = game_settings.player_jump_sound

    def set_movement(self, direction, move=True):

        self.frame_count = 0
        self.frame_wait = 0

        if move:
            self.facing_right = direction

            if direction:
                self.moving_right = True
            else:
                self.moving_left = True
            self.max_fc = self.walking_f.fc
        else:
            if not direction:
                self.moving_left = False
            else:
                self.moving_right = False

            if not self.moving_right and not self.moving_left and not self.jumping and not self.shooting:
                self.max_fc = self.idle_f.fc

    def jump(self):

        if not self.jumping:
            pygame.mixer.Sound.play(self.player_jump_sound)
            self.jumping = True
            self.vel_y = self.vel_jump

    def land(self):

        self.jumping = False

        if self.moving_left or self.moving_right:
            self.max_fc = self.walking_f.fc
        else:
            self.max_fc = self.idle_f.fc

        if self.frame_count >= self.max_fc:
            self.frame_count = 0
            self.frame_wait = 0

    def hit(self):

        self.shooting = True
        self.max_fc = self.shooting_f.fc
        self.frame_count = 0
        self.frame_wait = 0

    def move(self):

        if self.moving_left or self.moving_right:

            if self.moving_right:
                self.x += self.vel_x
            else:
                self.x -= self.vel_x

            if not self.jumping and not self.shooting:
                self.current_frame = self.walking_f.frame(self.frame_count, self.facing_right)

        elif not self.jumping and not self.shooting:
            self.land()
            self.current_frame = self.idle_f.frame(self.frame_count, self.facing_right)

        if self.jumping and not self.shooting:
            self.current_frame = self.jumping_f.frame(self.frame_count, self.facing_right)

        if self.shooting:
            self.current_frame = self.shooting_f.frame(self.frame_count, self.facing_right)
            if self.frame_count is self.max_fc - 2:
                self.add_projectile()
        
        self.vel_y -= 3
        self.y = self.y - self.vel_y

        # Resets variables at ground
        if self.y > self.ground:
            self.y = self.ground
            self.jumping = False
            self.vel_y = 0

        for projectile in self.projectiles:
            projectile.set_frame(self.facing_right)
            if not projectile.move():
                self.projectiles.remove(projectile)

        self.frame_wait += 1
        self.frame_count = self.frame_wait // self.max_fc

        if self.frame_wait > self.max_fc * 10 or self.frame_count >= self.max_fc:
            self.frame_wait = 0
            self.frame_count = 0

        if self.shooting and self.frame_count is (self.max_fc - 1):
            self.frame_count = 0
            self.frame_wait = 0
            if self.moving_left or self.moving_right:
                self.max_fc = self.walking_f.fc
            elif self.jumping:
                self.max_fc = self.jumping.fc
            else:
                self.max_fc = self.idle_f.fc
            self.shooting = False

    def move_by_amount(self, x, y):
        # moves player by specified x and y number of pixels
        # used for collision testing
        self.x += x
        self.y += y

    def blitme(self):
        self.screen.blit(self.current_frame, (self.x, self.y, self.width, self.height))
        for projectile in self.projectiles:
            projectile.blitme()

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def check_collision(self, obj_rect):
        if self.get_rect().colliderect(obj_rect):
            return True
        return False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def reset(self, game_settings, x_spawn, y_spawn):
        self.health = game_settings.player_health
        self.x = x_spawn
        self.y = y_spawn
        self.jumping = False
        self.shooting = False
        self.moving_left = False
        self.moving_right = False
        self.frame_wait = 0
        self.frame_count = 0

    def load_frames(self, player_frames):
        self.idle_f.load_frames(player_frames['idle'], player_frames['file_type'])
        self.walking_f.load_frames(player_frames['walking'], player_frames['file_type'])
        self.jumping_f.load_frames(player_frames['jumping'], player_frames['file_type'])
        self.shooting_f.load_frames(player_frames['shooting'], player_frames['file_type'])
        self.proj_f.load_frames(player_frames['projectile'], player_frames['file_type'])

    def clear_frames(self):
        self.idle_f.clear()
        self.walking_f.clear()
        self.jumping_f.clear()
        self.shooting_f.clear()

    def add_projectile(self):
        if len(self.projectiles) >= self.proj_max:
            return

        if self.facing_right:
            dir_x = 1
        else:
            dir_x = -1

        self.projectiles.append(Projectile(
            self.screen, self.proj_f.copy(), self.x, self.y, dir_x, 0, 20))

    def collide_projectiles(self, obj):

        damage = 0
        # Checks if projectiles collide with object
        for projectile in self.projectiles:

            # Lowers health and removes if true
            if projectile.check_collision(obj.get_rect()):
                self.projectiles.remove(projectile)
                damage += projectile.damage

        return damage


class Frames:

    def __init__(self, size):

        self.r_frames = []
        self.l_frames = []

        self.size = size
        self.fc = None

    def load_frames(self, load, f_type):

        path = load['path']
        fc = load['fc']

        for frame in range(fc):

            self.r_frames.append(pygame.transform.smoothscale(
                pygame.image.load(path + str(frame) + f_type), self.size))
            self.l_frames.append(pygame.transform.flip(self.r_frames[frame], True, False))

        self.fc = len(self.r_frames)

    def frame(self, frame, direction):

        if direction:
            return self.r_frames[frame]
        else:
            return self.l_frames[frame]

    def clear(self):
        self.r_frames.clear()
        self.l_frames.clear()

    def copy(self):
        tmp = Frames(self.size)
        tmp.r_frames = self.r_frames.copy()
        tmp.l_frames = self.l_frames.copy()
        return tmp


class Projectile:

    def __init__(self, screen, frames, x, y, dir_x, dir_y, speed):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.x = x
        self.y = y + 33
        self.speed_x = dir_x * speed
        self.speed_y = dir_y * speed

        self.damage = 2

        self.frames = frames
        self.frame_count = 0
        self.current_frame = None

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Activates removal if off screen
        if (self.x > self.screen_rect.width or self.x < 0) or (
                self.y > self.screen_rect.height or self.y < 0):
            return 0    # Pop self
        return 1

    def check_collision(self, rect):
        return pygame.Rect(self.x, self.y, self.frames.size[0], self.frames.size[1]).colliderect(rect)

    def set_frame(self, direction):
        if self.frame_count >= 4:
            self.frame_count = 0

        if direction:
            self.current_frame = self.frames.frame(self.frame_count, direction)
        else:
            self.current_frame = self.frames.frame(self.frame_count, direction)

        self.frame_count += 1

    def blitme(self):
        self.screen.blit(self.current_frame, (self.x, self.y, self.frames.size[0], self.frames.size[1]))
