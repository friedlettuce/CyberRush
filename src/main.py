import sys

import pygame

from settings import Settings, GameState
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
        if gamestate is GameState.QUIT:
            sys.exit()
        elif gamestate is GameState.TITLE:
            gamestate = title_screen.check_events()
            title_screen.blitme()

        pygame.display.flip()


run_game()
