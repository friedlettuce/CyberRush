import pygame

from settings import Settings
import game_functions as gfn


def run_game():

    pygame.init()
    game_settings = Settings()

    screen = pygame.display.set_mode((
        game_settings.screen_w, game_settings.screen_h))
    pygame.display.set_caption(game_settings.game_name)

    while True:

        gfn.check_events()

        gfn.update_screen()


run_game()
