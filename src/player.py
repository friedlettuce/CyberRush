import pygame


class Player:

    def __init__(self, screen, game_settings, x ,y):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        
        # Initial Player Starting Point
        self.x = x
        self.y = y
        self.vel = game_settings.player_speed

    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel
    
    def blitme(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, 50, 50))
