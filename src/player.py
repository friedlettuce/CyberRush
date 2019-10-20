import pygame


class Player:

    def __init__(self, screen, game_settings, x, y):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.player_size = game_settings.player_size
        self.player_w = self.player_size[0]
        self.player_h = self.player_size[1]

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
        self.y = self.screen_ground = int((self.screen_rect.bottom / 1.5))
        self.vel = game_settings.player_speed

        # Flags for if there's maps available to the left or right
        self.map_left = False
        self.map_right = False
        # Flags if player has gone to another map
        self.off_left = False
        self.off_right = False
        
        # Flags for if player is moving/facing left/right, idle, walking
        self.facing_right = True
        self.moving_left = False
        self.moving_right = False
        self.idle = True
        self.walking = False

        # Inits frame
        self.frame_count = 0
        self.current_frame = self.idle_r_frames[self.frame_count]
        
        # Init Controls
        self.input = game_settings.input
        
    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[self.input['left']]:

            if (self.x - self.vel) < self.screen_rect.left and self.map_left:
                self.x -= self.vel
                self.off_left = True
            elif (self.x - self.vel) >= self.screen_rect.left:
                # Stops player from moving left bound, without left screen
                self.x -= self.vel

            self.current_frame = self.walk_l_frames[self.frame_count]

            # For idle frames
            self.facing_right = False

        elif keys[self.input['right']]:

            if (self.x + self.player_w + self.vel) > self.screen_rect.right and self.map_right:
                self.x += self.vel
                self.off_right = True
            elif (self.x + self.player_w + self.vel) <= self.screen_rect.right:
                self.x += self.vel

            self.current_frame = self.walk_r_frames[self.frame_count]

            self.facing_right = True

        else:

            if self.facing_right:
                self.current_frame = self.idle_r_frames[self.frame_count]
            else:
                self.current_frame = self.idle_l_frames[self.frame_count]

        if keys[self.input['up']] and (self.y - self.vel > 0):
            self.y -= self.vel
        elif keys[self.input['down']] and self.y + self.vel < self.screen_ground:
            self.y += self.vel

        self.frame_count += 1
        self.frame_count %= 8
    
    def blitme(self):
        self.screen.blit(self.current_frame, (self.x, self.y, self.player_w, self.player_h))
