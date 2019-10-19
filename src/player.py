import pygame


class Player:

    def __init__(self, screen, game_settings, x, y):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.player_w = game_settings.player_w
        self.player_h = game_settings.player_h
        
        # Initial Player Starting Point
        self.x = x
        self.y = self.screen_ground = int((self.screen_rect.bottom / 1.25))
        self.vel = game_settings.player_speed

        # Flags for if there's maps available to the left or right
        self.map_left = False
        self.map_right = False
        # Flags if player has gone to another map
        self.off_left = False
        self.off_right = False
        
        # Flags for if player is facing left or right
        self.facing_left = False
        self.facing_right = True

    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:

            if (self.x - self.vel) < self.screen_rect.left and self.map_left:
                self.x -= self.vel
                self.off_left = True
            elif (self.x - self.vel) >= self.screen_rect.left:
                # Stops player from moving left bound, without left screen
                self.x -= self.vel
                
            self.facing_left = True
            self.facing_right = False

        elif keys[pygame.K_RIGHT]:

            if (self.x + self.player_w + self.vel) > self.screen_rect.right and self.map_right:
                self.x += self.vel
                self.off_right = True
            elif (self.x + self.player_w + self.vel) <= self.screen_rect.right:
                self.x += self.vel
            
            self.facing_left = False
            self.facing_right = True

        if keys[pygame.K_UP] and (self.y - self.vel > 0):
            self.y -= self.vel
        elif keys[pygame.K_DOWN] and self.y + self.vel < self.screen_ground:
            self.y += self.vel
    
    def blitme(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, self.player_w, self.player_h))
