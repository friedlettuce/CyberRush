import pygame
from enum import Enum

from settings import Settings
import game_functions as gfn
from graphics import TitleScreen


def run_game():

    pygame.init()
    gamestate = GameState(0)
    game_settings = Settings()

    screen = pygame.display.set_mode((
        game_settings.screen_w, game_settings.screen_h))
    pygame.display.set_caption(game_settings.game_name)

    title_screen = TitleScreen(screen, game_settings)

    while True:

        gfn.check_events()

        gfn.update_screen(title_screen)


class GameState(Enum):
    TITLE = 0
    SETTINGS = 1
    ABOUT = 2
    PLAYING = 3
    SCORE = 4


run_game()
