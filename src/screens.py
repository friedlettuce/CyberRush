import pygame
import os

from settings import GameState
from mobs import Enemy, HoveringEnemy
from highscores import populateWithPlaceholders, initialDatabaseCreation, returnAScore, return5Scores, returnscoreavg, resetHighscores


# NOTE: Need to edit the number of buttons in game settings, need to add a new one for high scores screen

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
        # ADDED THIS LINE
        self.highscores_button = Button(
            screen, game_settings.highscores_path, int(self.screen_rect.centerx * 1.5),
            int(self.screen_rect.height - (button_num * self.screen_rect.height) / (game_settings.num_buttons + 1)))

        button_num -= 1

        self.quit_button = Button(
            screen, game_settings.quit_path, int(self.screen_rect.centerx * 1.5),
            int(self.screen_rect.height - (button_num * self.screen_rect.height) / (game_settings.num_buttons + 1)))

        self.buttons = [self.play_button, self.settings_button, self.about_button, self.highscores_button,
                        self.quit_button]

        self.Robot1 = HoveringEnemy(screen, game_settings, 0, (self.screen_rect.centery * 1.25),
                                    game_settings.hov_size[0], game_settings.hov_size[0],
                                    (self.screen_rect.centerx / 1.25))
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
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound)
                    ret_game_state = GameState.PLAYING
                elif self.settings_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound)
                    ret_game_state = GameState.SETTINGS
                elif self.about_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound)
                    ret_game_state = GameState.ABOUT
                elif self.highscores_button.image_rect.colliderect(
                        mouse_pos):  # ADDED THIS, IF BUTTON IS CLICKED GOES TO THIS EVENT
                    ret_game_state = GameState.HIGHSCORES
                elif self.quit_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound)
                    ret_game_state = GameState.QUIT

        print(ret_game_state)
        return ret_game_state

    def blitme(self):
        # Draws Title/Background/Buttons

        self.screen.blit(self.background_img, self.background_rect)

        self.screen.blit(self.title_img, self.title_rect)

        self.play_button.blitme()
        self.settings_button.blitme()
        self.about_button.blitme()
        self.highscores_button.blitme()
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

        # Projectile Settings
        self.left_change_projectile_button = Button(
            screen, game_settings.vol_up_path, int(self.screen_rect.centerx * 1.7),
            int(self.screen_rect.centery * 1.3))
        self.right_change_projectile_button = Button(
            screen, game_settings.vol_down_path, int(self.screen_rect.centerx * 1.3),
            int(self.screen_rect.centery * 1.3))

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

        self.control_melee_button = Button(
            screen, game_settings.control_button_path,
            int(self.screen_rect.centerx), int(self.screen_rect.centery * 1.6))
        self.control_melee_button_2 = Button(
            screen, game_settings.control_button_path2,
            int(self.screen_rect.centerx), int(self.screen_rect.centery * 1.6))

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
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound)
                    ret_game_state = GameState.TITLE

                # Volume buttons
                elif self.vol_down_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound_2)

                    self.game_settings.control_flag = True

                    self.game_settings.music_volume -= .025

                    if self.game_settings.music_volume < 0:
                        self.game_settings.music_volume = 0
                    pygame.mixer.music.set_volume(self.game_settings.music_volume)

                elif self.vol_up_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound_2)

                    self.game_settings.control_flag = True

                    self.game_settings.music_volume += .025

                    if self.game_settings.music_volume > 1:
                        self.game_settings.music_volume = 1
                    pygame.mixer.music.set_volume(self.game_settings.music_volume)

                elif self.control_up_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound_2)

                    self.control_up_button_2.blitme()
                    pygame.display.update()

                    self.game_settings.change_control('up')

                elif self.control_left_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound_2)

                    self.control_left_button_2.blitme()
                    pygame.display.update()


                    self.game_settings.change_control('left')

                elif self.control_down_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound_2)

                    self.control_down_button_2.blitme()
                    pygame.display.update()

                    self.game_settings.change_control('right')

                elif self.control_right_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound_2)

                    self.control_right_button_2.blitme()
                    pygame.display.update()

                    self.game_settings.change_control('shoot')

                elif self.control_melee_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound_2)

                    self.control_melee_button_2.blitme()
                    pygame.display.update()

                    self.game_settings.change_control('melee')

                elif self.reset_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound_2)

                    self.game_settings.default_settings()

                elif self.left_change_player_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound_2)

                    self.game_settings.change_player(1, None)

                elif self.right_change_player_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound_2)

                    self.game_settings.change_player(0, None)

                elif self.left_change_projectile_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound_2)

                    self.game_settings.change_player(None, 1)

                elif self.right_change_projectile_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound_2)

                    self.game_settings.change_player(None, 0)

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
        self.control_melee_button.blitme()

        # Default Settings Button
        self.reset_button.blitme()

        # Change Player Buttons
        self.left_change_player_button.blitme()
        self.right_change_player_button.blitme()

        # Change Player Projectile Buttons
        self.left_change_projectile_button.blitme()
        self.right_change_projectile_button.blitme()

        self.player_display()

    def control_display(self):
        large_text = pygame.font.Font(self.game_settings.cb2_path, 25)

        key = pygame.key.name(self.game_settings.input['shoot'])
        key = key.upper()
        
        ranged_control = large_text.render((str('Ranged Attack: ') + str(key)), True, (0, 0, 0))
        self.screen.blit(ranged_control, (int(self.screen_rect.centerx / 7), int(self.screen_rect.centery / 1*1.75)))

        key = pygame.key.name(self.game_settings.input['melee'])
        key = key.upper()

        melee_control = large_text.render((str('Melee Attack: ') + str(key)), True, (0, 0, 0))
        self.screen.blit(melee_control, (int(self.screen_rect.centerx + 20), int(self.screen_rect.centery * 1.55)))

        key = pygame.key.name(self.game_settings.input['left'])
        key = key.upper()

        left_control = large_text.render((str("Left Control: ") + str(key)), True, (0, 0, 0))
        self.screen.blit(left_control, (int(self.screen_rect.centerx / 7), int(self.screen_rect.centery / 1*1.25)))

        key = pygame.key.name(self.game_settings.input['up'])
        key = key.upper()

        up_control = large_text.render((str("Jump Control: ") + str(key)), True, (0, 0, 0))
        self.screen.blit(up_control, (int(self.screen_rect.centerx / 7), int(self.screen_rect.centery / 1*1)))

        key = pygame.key.name(self.game_settings.input['right'])
        key = key.upper()

        down_control = large_text.render(str("Right Control: " + str(key)), True, (0, 0, 0))
        self.screen.blit(down_control, (int(self.screen_rect.centerx / 7), int(self.screen_rect.centery / 1*1.5)))

    def volume_display(self):

        large_text = pygame.font.Font(self.game_settings.cb2_path, 25)
        volume_display = self.game_settings.music_volume*100
        
        volume_display = large_text.render((str(round(volume_display, 2)) + "%"), True, (0, 0, 0))
        self.screen.blit(volume_display, (int(self.screen_rect.centerx / 1.25), int(self.screen_rect.centery / 1.7)))

    def player_display(self):
        large_text = pygame.font.Font(self.game_settings.cb2_path, 25)
        small_text = pygame.font.Font(self.game_settings.cb2_path, 15)
        player = self.game_settings.player_skin + 1
        projectile = self.game_settings.player_projectile + 1

        player_display = large_text.render(("Player Skin: " + str(player)), True, (0, 0, 0))
        self.screen.blit(player_display, (int(self.screen_rect.centerx * 1.25), int(self.screen_rect.centery / 3)))

        projectile_display = large_text.render(("Projectile: " + str(projectile)), True, (0, 0, 0))
        self.screen.blit(projectile_display, (int(self.screen_rect.centerx * 1.25), int(self.screen_rect.centery / 1)))

        if self.game_settings.player_skin == 0:

            self.screen.blit(pygame.transform.scale(pygame.image.load(self.game_settings.Player_Preview_1_path),
                self.game_settings.player_size), (int(self.screen_rect.centerx * 1.42),
                int(self.screen_rect.centery / 1.7)))
        elif self.game_settings.player_skin == 1:

            self.screen.blit(pygame.transform.scale(pygame.image.load(self.game_settings.Player_Preview_2_path),
                self.game_settings.player_size), (int(self.screen_rect.centerx * 1.42),
                int(self.screen_rect.centery / 1.7)))

        if self.game_settings.player_projectile == 0:

            self.screen.blit(pygame.transform.scale(pygame.image.load(self.game_settings.Projectile_Preview_1_path),
                (33, 11)),(int(self.screen_rect.centerx * 1.45), int(self.screen_rect.centery * 1.3)))
        elif self.game_settings.player_projectile == 1:

            self.screen.blit(pygame.transform.scale(pygame.image.load(self.game_settings.Projectile_Preview_2_path),
                (33, 11)), (int(self.screen_rect.centerx * 1.45), int(self.screen_rect.centery * 1.3)))


class AboutScreen(Screen):

    def __init__(self, screen, game_settings):
        super().__init__(screen, game_settings)

        self.mainmenu_button = Button(
            screen, game_settings.mainmenu_path, int(self.screen_rect.centerx - 100),
            int(self.screen_rect.centery * 1.9))

        self.credits_button = Button(
            screen, game_settings.credits_path, int(self.screen_rect.centerx + 100),
            int(self.screen_rect.centery * 1.9))

    def check_events(self):

        ret_game_state = GameState(2)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                ret_game_state = GameState.QUIT

            elif event.type == pygame.MOUSEBUTTONUP:

                mouse_pos = pygame.Rect((pygame.mouse.get_pos()), (0, 0))

                if self.mainmenu_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound)
                    ret_game_state = GameState.TITLE

                elif self.credits_button.image_rect.colliderect(mouse_pos):
                    pygame.mixer.Sound.play(self.game_settings.button_click_sound)
                    os.startfile("Resources.txt")


        return ret_game_state

    def display_about(self):
        large_text = pygame.font.Font(self.game_settings.cb2_path, 25)
        medium_text = pygame.font.Font(self.game_settings.cb2_path, 20)

        line_1 = large_text.render(("A Software Engineering Project Made By: ") , True, (0, 0, 0))
        self.screen.blit(line_1, (int(self.screen_rect.centerx/3), int(self.screen_rect.centery / 3)))

        line_2 = large_text.render(("-Garett Anderson"), True, (0, 0, 0))
        self.screen.blit(line_2, (int(self.screen_rect.centerx / 3), int(self.screen_rect.centery / 1.5)))

        line_3 = large_text.render(("-Daniel Brown"), True, (0, 0, 0))
        self.screen.blit(line_3, (int(self.screen_rect.centerx / 3), int(self.screen_rect.centery / 1.15)))

        line_4 = large_text.render(("-Cameron Heffelfinger"), True, (0, 0, 0))
        self.screen.blit(line_4, (int(self.screen_rect.centerx / 3), int(self.screen_rect.centery * 1.05)))

        line_5 = large_text.render(("-Jared Usher"), True, (0, 0, 0))
        self.screen.blit(line_5, (int(self.screen_rect.centerx / 3), int(self.screen_rect.centery * 1.25)))

    def blitme(self):
        self.screen.fill(self.bk_color)

        self.display_about()
        self.mainmenu_button.blitme()
        self.credits_button.blitme()



class HighScoresScreen(Screen):

    def __init__(self, screen, game_settings):
        super().__init__(screen, game_settings)
        initialDatabaseCreation()
        self.scoreIndex = 0  # Will hold the score index for the page displayed

        self.mainmenu_button = Button(
            screen, game_settings.mainmenu_path, int(self.screen_rect.centerx),
            int(self.screen_rect.centery * 1.9))

        # Button will add placeholders to the high scores list for demo purposes
        self.addplaceholders_button = Button(
            screen, game_settings.placeholder_path, int(self.screen_rect.centerx * .3),
            int(self.screen_rect.centery * 1.9))

        # Button will index to next page of high scores
        self.nextpagebutton = Button(
            screen, game_settings.vol_up_path, int(self.screen_rect.centerx + 65),
            int(self.screen_rect.centery + 120))

        # Button will index to previous page of high scores
        self.prevpagebutton = Button(
            screen, game_settings.vol_down_path, int(self.screen_rect.centerx - 65),
            int(self.screen_rect.centery + 120))

        '''
        # Volume text
        text = "Change Volume"
        large_text = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurface = large_text.render(text, True, (0, 0, 0))
        self.TextRect = self.textSurface.get_rect()
        self.TextRect.center = ((self.screen_rect.centerx / 2), (self.screen_rect.centery / 3))
        '''
        #firstscore = returnAScore()  # First score contains a tuple, [0] is the entry name [1] is the score
        #entry = firstscore[0] + " " + str(firstscore[1])  # Converts the entry to a string to be displayed


        fivescores = return5Scores(self.scoreIndex)


        # Case of empty highscores list, inputs 5 placeholder values
        if fivescores is None:
            populateWithPlaceholders()


        # Maybe do fivescores[self.scoreIndex]
        score1 = fivescores[0]  # Each contains a tuple (playername, playerscore)

        try:
            score2 = fivescores[1]
        except(IndexError):
            pass
        try:
            score3 = fivescores[2]
        except(IndexError):
            pass
        try:
            score4 = fivescores[3]
        except(IndexError):
            pass
        try:
            score5 = fivescores[4]
        except(IndexError):
            pass


        try:
            entry1 = score1[0] + "  " + str(score1[1])
        except(UnboundLocalError):
            pass
        try:
            entry2 = score2[0] + "  " + str(score2[1])
        except(UnboundLocalError):
            pass
        try:
            entry3 = score3[0] + "  " + str(score3[1])
        except(UnboundLocalError):
            pass
        try:
            entry4 = score4[0] + "  " + str(score4[1])
        except(UnboundLocalError):
            pass
        try:
            entry5 = score5[0] + "  " + str(score5[1])
        except(UnboundLocalError):
            pass

        # Will display the average score in the top right
        text = "Score Average:" + str(round(returnscoreavg(), 2))
        scoreavg = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurfaceAvg = scoreavg.render(text, True, (0, 0, 0))
        self.TextRect6 = self.textSurfaceAvg.get_rect()
        self.TextRect6.center = ((self.screen_rect.centerx + 280), (self.screen_rect.centery - 190))

        # The following text will display the first top 5 scores on the screen
        text = entry1
        score1 = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurface1 = score1.render(text, True, (0, 0, 0))
        self.TextRect1 = self.textSurface1.get_rect()
        self.TextRect1.center = ((self.screen_rect.centerx), (self.screen_rect.centery - 150))

        try:
            text = entry2
            score2 = pygame.font.Font(self.game_settings.cb2_path, 25)
            self.textSurface2 = score2.render(text, True, (0, 0, 0))
            self.TextRect2 = self.textSurface2.get_rect()
            self.TextRect2.center = ((self.screen_rect.centerx), (self.screen_rect.centery - 100))
        except(UnboundLocalError):
            pass
        try:
            text = entry3
            score3 = pygame.font.Font(self.game_settings.cb2_path, 25)
            self.textSurface3 = score3.render(text, True, (0, 0, 0))
            self.TextRect3 = self.textSurface3.get_rect()
            self.TextRect3.center = ((self.screen_rect.centerx), (self.screen_rect.centery - 50))
        except(UnboundLocalError):
            pass

        try:
            text = entry4
            score4 = pygame.font.Font(self.game_settings.cb2_path, 25)
            self.textSurface4 = score4.render(text, True, (0, 0, 0))
            self.TextRect4 = self.textSurface4.get_rect()
            self.TextRect4.center = ((self.screen_rect.centerx), (self.screen_rect.centery))
        except(UnboundLocalError):
            pass

        try:
            text = entry5
            score5 = pygame.font.Font(self.game_settings.cb2_path, 25)
            self.textSurface5 = score5.render(text, True, (0, 0, 0))
            self.TextRect5 = self.textSurface5.get_rect()
            self.TextRect5.center = ((self.screen_rect.centerx), (self.screen_rect.centery + 50))
        except(UnboundLocalError):
            pass

    # Function indexes and displays the next page of scores
    def advance_page(self):
        self.scoreIndex += 1    # Add 1 to access next page of scores
        fivescores = return5Scores(self.scoreIndex)
        score1 = fivescores[0]
        score2 = fivescores[1]
        score3 = fivescores[2]
        score4 = fivescores[3]
        score5 = fivescores[4]
        entry1 = score1[0] + "  " + str(score1[1])
        entry2 = score2[0] + "  " + str(score2[1])
        entry3 = score3[0] + "  " + str(score3[1])
        entry4 = score4[0] + "  " + str(score4[1])
        entry5 = score5[0] + "  " + str(score5[1])

        text = entry1
        score1 = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurface1 = score1.render(text, True, (0, 0, 0))
        self.TextRect1 = self.textSurface1.get_rect()
        self.TextRect1.center = ((self.screen_rect.centerx), (self.screen_rect.centery - 150))

        text = entry2
        score2 = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurface2 = score2.render(text, True, (0, 0, 0))
        self.TextRect2 = self.textSurface2.get_rect()
        self.TextRect2.center = ((self.screen_rect.centerx), (self.screen_rect.centery - 100))

        text = entry3
        score3 = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurface3 = score3.render(text, True, (0, 0, 0))
        self.TextRect3 = self.textSurface3.get_rect()
        self.TextRect3.center = ((self.screen_rect.centerx), (self.screen_rect.centery - 50))

        text = entry4
        score4 = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurface4 = score4.render(text, True, (0, 0, 0))
        self.TextRect4 = self.textSurface4.get_rect()
        self.TextRect4.center = ((self.screen_rect.centerx), (self.screen_rect.centery))

        text = entry5
        score5 = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurface5 = score5.render(text, True, (0, 0, 0))
        self.TextRect5 = self.textSurface5.get_rect()
        self.TextRect5.center = ((self.screen_rect.centerx), (self.screen_rect.centery + 50))



    # Function decrements to the previous page of scores
    def previous_page(self):
        if self.scoreIndex <= 0:
            return
        self.scoreIndex -= 1
        fivescores = return5Scores(self.scoreIndex)
        score1 = fivescores[0]
        score2 = fivescores[1]
        score3 = fivescores[2]
        score4 = fivescores[3]
        score5 = fivescores[4]
        entry1 = score1[0] + "  " + str(score1[1])
        entry2 = score2[0] + "  " + str(score2[1])
        entry3 = score3[0] + "  " + str(score3[1])
        entry4 = score4[0] + "  " + str(score4[1])
        entry5 = score5[0] + "  " + str(score5[1])

        text = entry1
        score1 = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurface1 = score1.render(text, True, (0, 0, 0))
        self.TextRect1 = self.textSurface1.get_rect()
        self.TextRect1.center = ((self.screen_rect.centerx), (self.screen_rect.centery - 150))

        text = entry2
        score2 = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurface2 = score2.render(text, True, (0, 0, 0))
        self.TextRect2 = self.textSurface2.get_rect()
        self.TextRect2.center = ((self.screen_rect.centerx), (self.screen_rect.centery - 100))

        text = entry3
        score3 = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurface3 = score3.render(text, True, (0, 0, 0))
        self.TextRect3 = self.textSurface3.get_rect()
        self.TextRect3.center = ((self.screen_rect.centerx), (self.screen_rect.centery - 50))

        text = entry4
        score4 = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurface4 = score4.render(text, True, (0, 0, 0))
        self.TextRect4 = self.textSurface4.get_rect()
        self.TextRect4.center = ((self.screen_rect.centerx), (self.screen_rect.centery))

        text = entry5
        score5 = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurface5 = score5.render(text, True, (0, 0, 0))
        self.TextRect5 = self.textSurface5.get_rect()
        self.TextRect5.center = ((self.screen_rect.centerx), (self.screen_rect.centery + 50))



    def check_events(self):

        ret_game_state = GameState(4)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                ret_game_state = GameState.QUIT

            elif event.type == pygame.MOUSEBUTTONUP:

                mouse_pos = pygame.Rect((pygame.mouse.get_pos()), (0, 0))

                if self.mainmenu_button.image_rect.colliderect(mouse_pos):
                    ret_game_state = GameState.TITLE

                elif self.addplaceholders_button.image_rect.colliderect(mouse_pos):
                    # Call the populate with placeholders function inside highscores.py
                    populateWithPlaceholders()

                elif self.nextpagebutton.image_rect.colliderect(mouse_pos):
                    # Advance the page
                    self.advance_page()

                elif self.prevpagebutton.image_rect.colliderect(mouse_pos):
                    # Decrement the page
                    self.previous_page()

        return ret_game_state

    ''''
    def displayHighScores(self):
        firstscore = returnAScore()
        text = firstscore
        score1 = pygame.font.Font(self.game_settings.cb2_path, 25)
        self.textSurface1 = score1.render(text, True, (0, 0, 0))
        self.TextRect1 = self.textSurface1.get_rect()
        self.TextRect1.center = ((self.screen_rect.centerx), (self.screen_rect.centery - 150))
        '''

    # large_text = pygame.font.Font(self.game_settings.cb2_path, 25)
    # firstScore = returnAScore()
    # self.textSurface = large_text.render(firstScore, True, (0, 0, 0))

    def blitme(self):
        self.screen.fill(self.bk_color)
        try:
            self.screen.blit(self.textSurface1, self.TextRect1)
        except(AttributeError):
            pass
        try:
            self.screen.blit(self.textSurface2, self.TextRect2)
        except(AttributeError):
            pass
        try:
            self.screen.blit(self.textSurface3, self.TextRect3)
        except(AttributeError):
            pass
        try:
            self.screen.blit(self.textSurface4, self.TextRect4)
        except(AttributeError):
            pass
        try:
            self.screen.blit(self.textSurface5, self.TextRect5)
        except(AttributeError):
            pass

        self.screen.blit(self.textSurfaceAvg, self.TextRect6)

        self.mainmenu_button.blitme()
        self.addplaceholders_button.blitme()
        self.nextpagebutton.blitme()
        self.prevpagebutton.blitme()
        #self.credits_button.blitme()



