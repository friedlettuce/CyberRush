import pygame, copy

from settings import GameState
from player import Player
from mobs import HoveringEnemy
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

        # Stores maps and sets first map to city street
        self.maps = [self.city_street]

        # Temp Map
        self.maps.append(Map(screen, game_settings,
                game_settings.city_background_path, "City Street"))

        # Tentative space to spawn enemy for demo
        self.Robot1 = HoveringEnemy(screen, game_settings, int(self.screen_rect.width * .75), (
                self.screen_rect.centery / 2), game_settings.hov_size[0], game_settings.hov_size[0],
                    0, self.screen_rect.centery * 1.2)
        self.maps[0].add_enemy(self.Robot1)

        self.map = self.city_street
        self.map_counter = 0
        # Flags for if there's maps available to the left or right
        self.map_left = False
        self.map_right = False

    def screen_start(self):
        pygame.mixer.music.stop()
        self.pos(0)
        self.player.x = self.player.screen_rect.right / 8

    def pos(self, side):
        # When first displaying player on a map, loads the player at either spawn positions of map
        if not side:
            self.player.x = self.screen_rect.right + int(self.player.player_w / 2)
        else:
            self.player.x = self.player.screen_rect.left - int(self.player.player_w / 2)

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
            self.pos(0)
            self.player.off_left = False

        elif self.player.off_right:
            self.map_counter += 1
            self.map = self.maps[self.map_counter]
            self.pos(1)
            self.player.off_right = False

        self.player.move()

        return ret_game_state

    def screen_end(self):
        pass

    def blitme(self):

        self.map.blitme()
        self.player.blitme()
