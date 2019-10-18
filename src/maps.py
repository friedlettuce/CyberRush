import pygame
from player import Player


class CityStreet:

    def __init__(self, screen, game_settings):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Load and scale image
        self.img = pygame.image.load(game_settings.city_background_path)
        self.img = pygame.transform.scale(
            self.img, (game_settings.screen_w, game_settings.screen_h))

        self.img_rect = self.img.get_rect()
        self.img_rect.centerx = self.screen_rect.centerx
        self.img_rect.centery = self.screen_rect.centery
        
        self.Player = Player(self.screen, game_settings, 0, 0)

    def blitme(self):

        self.screen.blit(self.img, self.img_rect)
        self.Player.move(self.screen)
        self.Player.blitme(self.screen)
