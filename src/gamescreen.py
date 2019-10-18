import pygame

from settings import GameState
from player import Player
from maps import Map


class GameScreen(object):

    def __init__(self, screen, game_settings):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.game_settings = game_settings

        self.Player = Player(self.screen, game_settings, 0, 0)

        # Stores maps in map list (Load Map, Store in maps)
        self.city_street = Map(screen, game_settings,
                                      game_settings.city_background_path)
        self.maps = [self.city_street]

        # Sets first map to city street
        self.map = self.city_street

    def screen_start(self):
        pygame.mixer.music.stop()

    def screen_end(self):
        pass

    def check_events(self):

        ret_game_state = GameState(3)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                ret_game_state = GameState.QUIT

        return ret_game_state

    def blitme(self):
        self.map.blitme()

        self.Player.move()
        self.Player.blitme()
