import pygame


class TitleScreen:

    def __init__(self, screen, game_settings):

        self.screen = screen

        # Text display for the title (font/text/color)
        title_font = pygame.font.SysFont(
            game_settings.title_font, game_settings.title_size, True)
        self.title_text = self.text = title_font.render(
            game_settings.game_name, True, game_settings.title_color)
        self.title_rect = self.title_text.get_rect()

        # Add buttons/texts

    def blitme(self):
        # Draws Title/Background/Buttons

        self.screen.blit(self.title_text, self.title_rect)

