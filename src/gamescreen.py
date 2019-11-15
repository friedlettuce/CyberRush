from os import path
import pygame

from settings import GameState
from player import Player
from maps import Map


class GameScreen(object):

    def __init__(self, screen, game_settings):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.game_settings = game_settings
        self.input = game_settings.input

        # Map
        level_path = path.dirname(path.realpath("resources"))
        self.map = Map(self.screen, self.game_settings, path.join(level_path, 'level_01.txt'))

        self.player = Player(self.screen, game_settings, self.map.spawnpoint[0], self.map.spawnpoint[1])

    def screen_start(self):
        pygame.mixer.music.stop()

        # Sets player keys and spawn
        self.input = self.game_settings.input

    def check_events(self):

        ret_game_state = GameState(3)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                ret_game_state = GameState.QUIT

            elif event.type == pygame.KEYDOWN:

                if event.key == self.input['up']:
                    self.player.jump()
                    pass

                if event.key == self.input['left']:
                    self.player.move_left()

                if event.key == self.input['right']:
                    self.player.move_right()

            elif event.type == pygame.KEYUP:

                if event.key == self.input['left']:
                    self.player.move_left(False)

                if event.key == self.input['right']:
                    self.player.move_right(False)

        self.player.move()

        # Finds direction of any collision
        direction = self.map.collisions(self.player)
        if direction == 'left':
            self.player.x += self.player.vel
        elif direction == 'right':
            self.player.x -= self.player.vel
        elif direction == 'up':
            self.player.y += self.player.vel
        elif direction == 'down':
            self.player.y -= self.player.vel

        # Currently checks if player in shooting range
        self.map.update_enemies(self.player)

        return ret_game_state

    def screen_end(self):
        pass

    def blitme(self):

        self.map.blitme()
        self.player.blitme()
