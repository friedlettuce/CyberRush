import pygame

from settings import GameState
from player import Player
from maps import Map


class GameScreen(object):

    def __init__(self, screen, game_settings):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.game_settings = game_settings

        self.player = Player(self.screen, game_settings, 0, 0)

        # Stores maps in map list (Load Map, Store in maps)
        self.city_street = Map(screen, game_settings,
                game_settings.city_background_path, "City Street")
        self.maps = [self.city_street]
        self.player_map = game_settings.player_map

        # Sets first map to city street
        self.map = self.city_street
        self.map_counter = 0

    def screen_start(self):
        pygame.mixer.music.stop()
        self.pos_player(0)

    def pos_player(self, side):
        # When first displaying player on a map, loads the player at either spawn positions of map
        self.player.pos(self.player_map[self.map.name][side])

        if self.map_counter > 0:
            self.player.map_left = True
        else:
            self.player.map_left = False

        if self.map_counter < (len(self.maps) - 1):
            self.player.map_right = True
        else:
            self.player.map_right = False

    def check_events(self):

        ret_game_state = GameState(3)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                ret_game_state = GameState.QUIT

        if self.player.off_left:
            self.map_counter -= 1
            self.map = self.maps[self.map_counter]
            self.pos_player(1)
            self.player.off_left = False

        elif self.player.off_right:
            self.map_counter += 1
            self.map = self.maps[self.map_counter]
            self.pos_player(0)
            self.player.off_right = False

        self.player.move()

        return ret_game_state

    def screen_end(self):
        pass

    def blitme(self):

        self.map.blitme()
        self.player.blitme()
