import sys

import pygame

from settings import Settings, GameState
from screens import TitleScreen, SettingsScreen, AboutScreen, HighScoresScreen
from gamescreen import GameScreen


def run_game():
    pygame.init()
    cur_gamestate = GameState(1)
    new_gamestate = GameState(0)  # Used to track which game state we are switching to
    game_settings = Settings()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((
        game_settings.screen_w, game_settings.screen_h))
    pygame.display.set_caption(game_settings.game_name)

    title_screen = TitleScreen(screen, game_settings)
    settings_screen = SettingsScreen(screen, game_settings)
    about_screen = AboutScreen(screen, game_settings)

    game_settings.initialize_settings()
    game_screen = GameScreen(screen, game_settings)
    highscores_screen = HighScoresScreen(screen, game_settings)

    screens = {
        GameState.TITLE: title_screen,
        GameState.SETTINGS: settings_screen,
        GameState.ABOUT: about_screen,
        GameState.PLAYING: game_screen,
        GameState.HIGHSCORES: highscores_screen
    }

    screen = title_screen

    while True:

        clock.tick(game_settings.clock_tick_interval)

        if new_gamestate is GameState.QUIT:
            game_settings.save_settings()

            pygame.quit()
            sys.exit()

        if cur_gamestate != new_gamestate:
            # Run screen start function
            cur_gamestate = new_gamestate
            screen = screens[cur_gamestate]
            screen.screen_start()

        new_gamestate = screen.check_events()
        screen.update()
        screen.blitme()

        if cur_gamestate != new_gamestate:
            # If gamestate has changed, run screen end function
            screen.screen_end()

        pygame.display.flip()


run_game()