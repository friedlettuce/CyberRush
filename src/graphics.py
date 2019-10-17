import pygame
import sys

from settings import GameState


class TitleScreen:

    def __init__(self, screen, game_settings):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.bk_color = game_settings.bk_color

        # Image display for the title
        self.title_img = pygame.image.load(game_settings.title_path)
        self.title_rect = self.title_img.get_rect()

        self.title_rect.centerx = self.screen_rect.centerx / 2
        self.title_rect.centery = self.screen_rect.centery / 2

        # Buttons
        button_num = game_settings.num_buttons  # Tracks which button we're initializing
        self.play_button = Button(
            screen, game_settings.play_path, int(self.screen_rect.centerx * 1.5),
            int(self.screen_rect.height - (button_num * self.screen_rect.height) / (game_settings.num_buttons + 1)))

        button_num -= 1

        self.settings_button = Button(
            screen, game_settings.settings_path, int(self.screen_rect.centerx * 1.5),
            int(self.screen_rect.height - (button_num * self.screen_rect.height) / (game_settings.num_buttons + 1)))

        button_num -= 1

        self.about_button = Button(
            screen, game_settings.about_path, int(self.screen_rect.centerx * 1.5),
            int(self.screen_rect.height - (button_num * self.screen_rect.height) / (game_settings.num_buttons + 1)))

        button_num -= 1

        self.quit_button = Button(
            screen, game_settings.quit_path, int(self.screen_rect.centerx * 1.5),
            int(self.screen_rect.height - (button_num * self.screen_rect.height) / (game_settings.num_buttons + 1)))

        self.buttons = [self.play_button, self.settings_button, self.about_button, self.quit_button]

    def check_events(self):

        ret_game_state = GameState(0)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                ret_game_state = GameState.QUIT

            elif event.type == pygame.MOUSEBUTTONUP:

                mouse_pos = pygame.Rect((pygame.mouse.get_pos()), (0, 0))

                if self.play_button.image_rect.colliderect(mouse_pos):
                    ret_game_state = GameState.PLAYING
                elif self.settings_button.image_rect.colliderect(mouse_pos):
                    ret_game_state = GameState.SETTINGS
                elif self.about_button.image_rect.colliderect(mouse_pos):
                    ret_game_state = GameState.ABOUT
                elif self.quit_button.image_rect.colliderect(mouse_pos):
                    ret_game_state = GameState.QUIT

        return ret_game_state

    def blitme(self):
        # Draws Title/Background/Buttons

        self.screen.fill(self.bk_color)

        self.screen.blit(self.title_img, self.title_rect)

        self.play_button.blitme()
        self.settings_button.blitme()
        self.about_button.blitme()
        self.quit_button.blitme()


class Button:

    def __init__(self, screen, image_path, posx, posy):

        self.screen = screen
        self.image = pygame.image.load(image_path)

        self.image_rect = self.image.get_rect()
        self.image_rect.centerx = posx
        self.image_rect.centery = posy

    def blitme(self):
        self.screen.blit(self.image, self.image_rect)

class SettingsScreen:

    def __init__(self, screen, game_settings):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.bk_color = game_settings.bk_color

        self.mainmenu_button = Button(
            screen, game_settings.mainmenu_path, int(self.screen_rect.centerx),
            int(self.screen_rect.centery * 1.9))

    def check_events(self):

        ret_game_state = GameState(1)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                ret_game_state = GameState.QUIT

            elif event.type == pygame.MOUSEBUTTONUP:

                mouse_pos = pygame.Rect((pygame.mouse.get_pos()), (0, 0))

                if self.mainmenu_button.image_rect.colliderect(mouse_pos):
                    ret_game_state = GameState.TITLE

        return ret_game_state

    def blitme(self):
        self.screen.fill(self.bk_color)

        self.mainmenu_button.blitme()