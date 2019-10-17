import pygame

from settings import GameState
from maps import CityStreet


class GameScreen(object):

    def __init__(self, screen, game_settings):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.game_settings = game_settings

        self.city_street = CityStreet(screen, game_settings)

        text = "BOTTOM TEXT"

        large_text = pygame.font.Font(self.game_settings.cb2_path, 80)
        self.textSurface = large_text.render(text, True, (0, 0, 0))
        self.text_rect = self.textSurface.get_rect()
        self.text_rect.center = (self.screen_rect.centerx, self.screen_rect.centery)

    def check_events(self):

        ret_game_state = GameState(3)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                ret_game_state = GameState.QUIT

        return ret_game_state

    def blitme(self):

        self.city_street.blitme()
        self.screen.blit(self.textSurface, self.text_rect)
