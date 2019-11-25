import pygame

from settings import GameState
from mobs import Enemy, HoveringEnemy


class Screen:

    def __init__(self, screen, game_settings):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.game_settings = game_settings
        self.bk_color = game_settings.bk_color

    def screen_start(self):
        pass

    def update(self):
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
        self.background_img = pygame.transform.scale(
            self.background_img, (game_settings.screen_w, game_settings.screen_h))
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
        
        self.Robot1 = HoveringEnemy(screen, game_settings, 0, (self.screen_rect.centery*1.25),
                    game_settings.hov_size[0], game_settings.hov_size[0], (self.screen_rect.centerx/1.25))
        self.Robot2 = HoveringEnemy(screen, game_settings, self.screen_rect.centerx, 0,
                    game_settings.hov_size[0], game_settings.hov_size[0], 0, self.screen_rect.centery)

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
        
        self.Robot1.update()
        self.Robot2.update()
        self.Robot1.blitme()
        self.Robot2.blitme()


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

        # Player Settings
        self.left_change_player_button = Button(
            screen, game_settings.vol_up_path, int(self.screen_rect.centerx * 1.7),
            int(self.screen_rect.centery / 1.5))

        self.right_change_player_button = Button(
            screen, game_settings.vol_down_path, int(self.screen_rect.centerx * 1.3),
            int(self.screen_rect.centery / 1.5))

        # Volume text
        text = "Change Volume"
        large_text = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurface = large_text.render(text, True, (0, 0, 0))
        self.TextRect = self.textSurface.get_rect()
        self.TextRect.center = ((self.screen_rect.centerx / 2), (self.screen_rect.centery / 3))

        #  Buttons To Change Controls/Signal When Controls Are Being Changed
        self.control_up_button = Button(
            screen, game_settings.control_button_path,
            int(self.screen_rect.centerx / 10), int(self.screen_rect.centery * 1.05))
        self.control_up_button_2 = Button(
            screen, game_settings.control_button_path2,
            int(self.screen_rect.centerx / 10), int(self.screen_rect.centery * 1.05))

        self.control_left_button = Button(
            screen, game_settings.control_button_path,
            int(self.screen_rect.centerx / 10), int(self.screen_rect.centery * 1.3))
        self.control_left_button_2 = Button(
            screen, game_settings.control_button_path2,
            int(self.screen_rect.centerx / 10), int(self.screen_rect.centery * 1.3))

        self.control_down_button = Button(
            screen, game_settings.control_button_path,
            int(self.screen_rect.centerx / 10), int(self.screen_rect.centery * 1.55))
        self.control_down_button_2 = Button(
            screen, game_settings.control_button_path2,
            int(self.screen_rect.centerx / 10), int(self.screen_rect.centery * 1.55))

        self.control_right_button = Button(
            screen, game_settings.control_button_path,
            int(self.screen_rect.centerx / 10), int(self.screen_rect.centery * 1.8))
        self.control_right_button_2 = Button(
            screen, game_settings.control_button_path2,
            int(self.screen_rect.centerx / 10), int(self.screen_rect.centery * 1.8))

        self.reset_button = Button(
            screen, game_settings.reset_control_button_path,
            int(self.screen_rect.centerx * 1.5), int(self.screen_rect.centery * 1.9))

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

                    self.game_settings.control_flag = True

                    self.game_settings.music_volume -= .025

                    if self.game_settings.music_volume < 0:
                        self.game_settings.music_volume = 0
                    pygame.mixer.music.set_volume(self.game_settings.music_volume)

                elif self.vol_up_button.image_rect.colliderect(mouse_pos):

                    self.game_settings.control_flag = True

                    self.game_settings.music_volume += .025

                    if self.game_settings.music_volume > 1:
                        self.game_settings.music_volume = 1
                    pygame.mixer.music.set_volume(self.game_settings.music_volume)

                elif self.control_up_button.image_rect.colliderect(mouse_pos):

                    self.control_up_button_2.blitme()
                    pygame.display.update()

                    self.game_settings.change_control('up')

                elif self.control_left_button.image_rect.colliderect(mouse_pos):

                    self.control_left_button_2.blitme()
                    pygame.display.update()

                    self.game_settings.change_control('left')

                elif self.control_down_button.image_rect.colliderect(mouse_pos):

                    self.control_down_button_2.blitme()
                    pygame.display.update()

                    self.game_settings.change_control('down')

                elif self.control_right_button.image_rect.colliderect(mouse_pos):

                    self.control_right_button_2.blitme()
                    pygame.display.update()

                    self.game_settings.change_control('right')

                elif self.reset_button.image_rect.colliderect(mouse_pos):

                    self.game_settings.default_settings()

                elif self.left_change_player_button.image_rect.colliderect(mouse_pos):

                    self.game_settings.change_player(2)

                elif self.right_change_player_button.image_rect.colliderect(mouse_pos):

                    self.game_settings.change_player(1)

        return ret_game_state

    def blitme(self):

        self.screen.fill(self.bk_color)

        self.screen.blit(self.textSurface, self.TextRect)

        self.mainmenu_button.blitme()

        # Volume Buttons
        self.vol_up_button.blitme()
        self.vol_down_button.blitme()
        
        # Volume Percentage
        self.volume_display()

        # Control Buttons
        self.control_display()
        self.control_up_button.blitme()
        self.control_left_button.blitme()
        self.control_down_button.blitme()
        self.control_right_button.blitme()

        # Default Settings Button
        self.reset_button.blitme()

        # Change Player Buttons
        self.left_change_player_button.blitme()
        self.right_change_player_button.blitme()

        self.player_display()

    def control_display(self):
        large_text = pygame.font.Font(self.game_settings.cb2_path, 25)

        key = pygame.key.name(self.game_settings.input['right'])
        key = key.upper()
        
        right_control = large_text.render((str('Right Control: ') + str(key)), True, (0, 0 ,0))
        self.screen.blit(right_control, (int(self.screen_rect.centerx / 7), int(self.screen_rect.centery / 1*1.75)))

        key = pygame.key.name(self.game_settings.input['left'])
        key = key.upper()

        left_control = large_text.render((str("Left Control: ") + str(key)), True, (0, 0 ,0))
        self.screen.blit(left_control, (int(self.screen_rect.centerx / 7), int(self.screen_rect.centery / 1*1.25)))

        key = pygame.key.name(self.game_settings.input['up'])
        key = key.upper()

        up_control = large_text.render((str("Jump Control: ") + str(key)), True, (0, 0 ,0))
        self.screen.blit(up_control, (int(self.screen_rect.centerx / 7), int(self.screen_rect.centery / 1*1)))

        key = pygame.key.name(self.game_settings.input['down'])
        key = key.upper()

        down_control = large_text.render(str("Down Control: " + str(key)), True, (0, 0 ,0))
        self.screen.blit(down_control, (int(self.screen_rect.centerx / 7), int(self.screen_rect.centery / 1*1.5)))

    def volume_display(self):

        large_text = pygame.font.Font(self.game_settings.cb2_path, 25)
        volume_display = self.game_settings.music_volume*100
        
        volume_display = large_text.render((str(round(volume_display, 2)) + "%"), True, (0, 0, 0))
        self.screen.blit(volume_display, (int(self.screen_rect.centerx / 1.25), int(self.screen_rect.centery / 1.7)))

    def player_display(self):
        large_text = pygame.font.Font(self.game_settings.cb2_path, 25)
        small_text = pygame.font.Font(self.game_settings.cb2_path, 15)
        player = self.game_settings.player_skin

        player_display = large_text.render(("Player Skin: " + str(player)), True, (0, 0, 0))
        self.screen.blit(player_display, (int(self.screen_rect.centerx * 1.25), int(self.screen_rect.centery / 3)))

        warning_display = small_text.render("Requires Restart", True, (0, 0, 0))
        self.screen.blit(warning_display, (int(self.screen_rect.centerx * 1.26), int(self.screen_rect.centery / 2.25)))

        if self.game_settings.player_skin == 1:
            self.screen.blit(pygame.image.load(self.game_settings.Player_Preview_1_path),
                             (int(self.screen_rect.centerx * 1.45), int(self.screen_rect.centery / 1.7)))
        elif self.game_settings.player_skin == 2:
            self.screen.blit(pygame.image.load(self.game_settings.Player_Preview_2_path),
                             (int(self.screen_rect.centerx * 1.45), int(self.screen_rect.centery / 1.7)))


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
        self.Robot3.blitme()
