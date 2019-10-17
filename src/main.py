import sys

import pygame

from settings import Settings, GameState
from graphics import TitleScreen, SettingsScreen, AboutScreen
from gamescreen import GameScreen


def run_game():

    pygame.init()
    gamestate = GameState(0)
    game_settings = Settings()
    
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((
        game_settings.screen_w, game_settings.screen_h))
    pygame.display.set_caption(game_settings.game_name)

    title_screen = TitleScreen(screen, game_settings)
    settings_screen = SettingsScreen(screen, game_settings)
    about_screen = AboutScreen(screen, game_settings)
    game_screen = GameScreen(screen, game_settings)

    while True:
        clock.tick(60)
        
        if gamestate is GameState.QUIT:
            sys.exit()

        elif gamestate is GameState.TITLE:
            gamestate = title_screen.check_events()
            title_screen.blitme()

        elif gamestate is GameState.SETTINGS:
            gamestate = settings_screen.check_events()
            settings_screen.blitme()

        elif gamestate is GameState.ABOUT:
            gamestate = about_screen.check_events()
            about_screen.blitme()

        elif gamestate is GameState.PLAYING:
            gamestate = game_screen.check_events()
            game_screen.blitme()           

        pygame.display.flip()


run_game()
