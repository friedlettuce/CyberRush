import pygame


class Player:

    def __init__(self, screen, game_settings, x, y):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.player_size = game_settings.player_size
        self.width = self.player_size[0]
        self.height = self.player_size[1]

        # Loads frames for player
        self.idle_r_frames = []
        self.idle_l_frames = []
        self.walk_r_frames = []
        self.walk_l_frames = []

        load_frames = game_settings.player_frames

        for frame in range(load_frames['idle_fc']):

            self.idle_r_frames.append(pygame.transform.scale(
                pygame.image.load(load_frames['idle_path'] + str(
                    frame) + load_frames['file_type']), self.player_size))
            self.idle_l_frames.append(pygame.transform.flip(self.idle_r_frames[frame], True, False))

        for frame in range(load_frames['walk_fc']):

            self.walk_r_frames.append(pygame.transform.scale(
                pygame.image.load(load_frames['walk_path'] + str(
                    frame) + load_frames['file_type']), self.player_size))
            self.walk_l_frames.append(pygame.transform.flip(self.walk_r_frames[frame], True, False))
        
        # Initial Player Starting Point
        self.x = x
        self.y = y
        self.ground = None
        self.vel = game_settings.player_speed
        self.vel_y = 0
        self.vel_jump = game_settings.player_jump
        
        # Flags for if player is moving/facing left/right, idle, walking
        self.facing_right = True
        self.moving_left = False
        self.moving_right = False
        self.jumping = False

        # Inits frame
        self.frame_count = 0
        self.current_frame = self.idle_r_frames[self.frame_count]

    def move_left(self, move=True):

        if move:
            self.moving_left = True
            self.facing_right = False
            self.moving_right = False
        else:
            self.moving_left = False

    def move_right(self, move=True):

        if move:
            self.moving_right = True
            self.facing_right = True
            self.moving_left = False
        else:
            self.moving_right = False

    def jump(self):

        if not self.jumping:
            self.jumping = True
            self.vel_y = self.vel_jump

    def move(self):
        
        if self.moving_left:

            self.x -= self.vel
            self.current_frame = self.walk_l_frames[self.frame_count]

            self.facing_right = False

        elif self.moving_right:

            self.x += self.vel
            self.current_frame = self.walk_r_frames[self.frame_count]

            self.facing_right = True

        else:

            if self.facing_right:
                self.current_frame = self.idle_r_frames[self.frame_count]
            else:
                self.current_frame = self.idle_l_frames[self.frame_count]
        

        self.y = self.y - self.vel_y
        self.vel_y -= 1

        # Resets variables at ground
        if self.y > self.ground:
            self.y = self.ground
            self.jumping = False
            self.vel_y = 0

        self.frame_count += 1
        self.frame_count %= 8

    def move_by_amount(self, x, y):
        #moves player by specified x and y number of pixels
        #used for collision testing
        self.x += x
        self.y += y

    def blitme(self):
        self.screen.blit(self.current_frame, (self.x, self.y, self.width, self.height))

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def collide_tleft(self):
        pass

    def collide_mleft(self):
        pass

    def collide_bleft(self):
        pass

    def collide_tright(self):
        pass

    def collide_mright(self):
        pass

    def collide_bright(self):
        pass

    def collide_tmid(self):
        pass

    def collide_bmid(self):
        pass
