import pygame, os

from settings import GameState
from mobs import HoveringEnemyX, HoveringEnemyY, Enemy


class Screen:

    def __init__(self, screen, game_settings):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.game_settings = game_settings
        self.bk_color = game_settings.bk_color

    def screen_start(self):
        pass

    def screen_end(self):
        pass


class TitleScreen(Screen):

    def __init__(self, screen, game_settings):
        super().__init__(screen, game_settings)

        # Image display for the title
        self.title_img = pygame.image.load(game_settings.title_path)
        self.title_rect = self.title_img.get_rect()

        self.title_rect.centerx = self.screen_rect.centerx / 2
        self.title_rect.centery = self.screen_rect.centery / 2

        # Image display for the background
        self.background_img = pygame.image.load(game_settings.title_background_path)
        self.background_rect = self.background_img.get_rect()

        self.background_rect.centerx = self.screen_rect.centerx
        self.background_rect.centery = self.screen_rect.centery

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
        
        self.Robot1 = HoveringEnemyX(game_settings, 0, 300, 150, 150, self.screen_rect.centerx)
        self.Robot2 = HoveringEnemyY(game_settings, self.screen_rect.centerx, 0, 150,150, self.screen_rect.centery)

    def screen_start(self):
        # Music
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.game_settings.titleMusic_path)
            pygame.mixer.music.set_volume(self.game_settings.music_volume)
            pygame.mixer.music.play(-1)

    def screen_end(self):
        # Temporary for now
        pass

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

        self.screen.blit(self.background_img, self.background_rect)

        self.screen.blit(self.title_img, self.title_rect)

        self.play_button.blitme()
        self.settings_button.blitme()
        self.about_button.blitme()
        self.quit_button.blitme()
        
        self.Robot1.blitme(self.screen)
        self.Robot2.blitme(self.screen)


class Button:

    def __init__(self, screen, image_path, posx, posy):

        self.screen = screen
        self.image = pygame.image.load(image_path)

        self.image_rect = self.image.get_rect()
        self.image_rect.centerx = posx
        self.image_rect.centery = posy

    def blitme(self):
        self.screen.blit(self.image, self.image_rect)


class SettingsScreen(Screen):

    def __init__(self, screen, game_settings):
        super().__init__(screen, game_settings)

        self.mainmenu_button = Button(
            screen, game_settings.mainmenu_path, int(self.screen_rect.centerx),
            int(self.screen_rect.centery * 1.9))

        # Volume settings
        self.vol_up_button = Button(
            screen, game_settings.vol_up_path, int(self.screen_rect.centerx / 1.5),
            int(self.screen_rect.centery / 1.5))

        self.vol_down_button = Button(
            screen, game_settings.vol_down_path, int(self.screen_rect.centerx / 2.5),
            int(self.screen_rect.centery / 1.5))

        # Volume text
        text = "Change Volume"
        largeText = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurface = largeText.render(text, True, (0, 0, 0))
        self.TextRect = self.textSurface.get_rect()
        self.TextRect.center = ((self.screen_rect.centerx / 2), (self.screen_rect.centery / 3))

    def check_events(self):

        ret_game_state = GameState(1)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                ret_game_state = GameState.QUIT

            elif event.type == pygame.MOUSEBUTTONUP:

                mouse_pos = pygame.Rect((pygame.mouse.get_pos()), (0, 0))

                if self.mainmenu_button.image_rect.colliderect(mouse_pos):
                    ret_game_state = GameState.TITLE

                # Volume buttons
                elif self.vol_down_button.image_rect.colliderect(mouse_pos):
                    self.game_settings.music_volume -= .025

                    if self.game_settings.music_volume < 0:
                        self.game_settings.music_volume = 0
                    pygame.mixer.music.set_volume(self.game_settings.music_volume)

                elif self.vol_up_button.image_rect.colliderect(mouse_pos):

                    self.game_settings.music_volume += .025

                    if self.game_settings.music_volume > 1:
                        self.game_settings.music_volume = 1
                    pygame.mixer.music.set_volume(self.game_settings.music_volume)

        return ret_game_state

    def blitme(self):

        self.screen.fill(self.bk_color)

        self.screen.blit(self.textSurface, self.TextRect)

        self.mainmenu_button.blitme()

        # Volume Buttons
        self.vol_up_button.blitme()
        self.vol_down_button.blitme()


class AboutScreen(Screen):

    def __init__(self, screen, game_settings):
        super().__init__(screen, game_settings)

        self.mainmenu_button = Button(
            screen, game_settings.mainmenu_path, int(self.screen_rect.centerx),
            int(self.screen_rect.centery * 1.9))

    def check_events(self):

        ret_game_state = GameState(2)

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
