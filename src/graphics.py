import pygame


class TitleScreen:

    def __init__(self, screen, game_settings):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Image display for the title
        self.title_img = pygame.image.load(game_settings.title_path)
        self.title_rect = self.title_img.get_rect()

        self.title_rect.centerx = self.screen_rect.centerx / 2
        self.title_rect.centery = self.screen_rect.centery / 2

        # Add buttons/texts
        play_button = Button(screen)

    def blitme(self):
        # Draws Title/Background/Buttons

        self.screen.blit(self.title_img, self.title_rect)


class Button:

    def __init__(self, screen):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

