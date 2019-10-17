import pygame

from settings import GameState
from maps import CityStreet


class GameScreen(object):

    def __init__(self, screen, game_settings):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.game_settings = game_settings

        self.city_street = CityStreet(screen, game_settings)

    def check_events(self):

        ret_game_state = GameState(3)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                ret_game_state = GameState.QUIT

        return ret_game_state

    def blitme(self):

        self.city_street.blitme()
