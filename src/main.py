import sys

import pygame

from settings import Settings, GameState
from graphics import TitleScreen, SettingsScreen, AboutScreen
from gamescreen import GameScreen


def run_game():

    pygame.init()
    cur_gamestate = GameState(1)
    new_gamestate = GameState(0)    # Used to track which game state we are switching to
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
        clock.tick(game_settings.clock_tick_interval)
        
        if new_gamestate is GameState.QUIT:
            pygame.quit()
            sys.exit()

        elif new_gamestate is GameState.TITLE:
            if cur_gamestate != new_gamestate:
                # Run screen start function
                cur_gamestate = new_gamestate
                title_screen.screen_start()
            new_gamestate = title_screen.check_events()
            title_screen.blitme()
            if cur_gamestate != new_gamestate:
                # If gamestate has changed, run screen end function
                title_screen.screen_end()

        elif new_gamestate is GameState.SETTINGS:
            if cur_gamestate != new_gamestate:
                # Run screen start function
                cur_gamestate = new_gamestate
            new_gamestate = settings_screen.check_events()
            settings_screen.blitme()
            #put screen_end function here if needed later

        elif new_gamestate is GameState.ABOUT:
            if cur_gamestate != new_gamestate:
                # Run screen start function
                cur_gamestate = new_gamestate
            new_gamestate = about_screen.check_events()
            about_screen.blitme()
            #put screen_end function here if needed later

        elif new_gamestate is GameState.PLAYING:
            if cur_gamestate != new_gamestate:
                # Run screen start function
                cur_gamestate = new_gamestate
            new_gamestate = game_screen.check_events()
            game_screen.blitme()    
            #put screen_end function here if needed later

        pygame.display.flip()


run_game()
