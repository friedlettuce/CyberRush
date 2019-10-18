import pygame


class Map:

    def __init__(self, screen, game_settings, background_path):
        # Maps can store the screen and background image for all maps

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Load, scale, and position background image
        self.bg = pygame.image.load(background_path)
        self.bg = pygame.transform.scale(
            self.bg, (game_settings.screen_w, game_settings.screen_h))

        self.bg_rect = self.bg.get_rect()
        self.bg_rect.centerx = self.screen_rect.centerx
        self.bg_rect.centery = self.screen_rect.centery

    def blitme(self):

        self.screen.blit(self.bg, self.bg_rect)


'''
Fill out class when class by class functionality arises

class CityStreet:

    def __init__(self, screen, game_settings, background_path):
        super().__init__(screen, game_settings, background_path)
'''