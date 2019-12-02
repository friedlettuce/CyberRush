import os, pygame
from enum import Enum


class Settings:

    def __init__(self):

        resources_folder = os.path.dirname(os.path.realpath("resources"))
        resources_folder = os.path.join(resources_folder, "resources")

        # Main Display Settings
        self.screen_w = 900
        self.screen_h = 450
        self.game_name = "Cyber Rush"

        # Title Screen Settings
        self.title_background_path = os.path.join(resources_folder, "title_bg.png")
        self.bk_color = (39, 184, 184)

        self.num_buttons = 5    #Changed this from 4 to 5
        self.title_path = os.path.join(resources_folder, "Title.bmp")
        self.play_path = os.path.join(resources_folder, "PlayButton.bmp")
        self.quit_path = os.path.join(resources_folder, "QuitButton.bmp")
        self.about_path = os.path.join(resources_folder, "AboutButton.bmp")
        self.highscores_path = os.path.join(resources_folder, "HighScoresButton.bmp")   # Added button to go to highscores screen
        self.placeholder_path = os.path.join(resources_folder, "PlaceholdersButton.bmp")    # Added button to add placeholders in highscores
        self.settings_path = os.path.join(resources_folder, "SettingsButton.bmp")
        self.mainmenu_path = os.path.join(resources_folder, "MainMenuButton.bmp")

        # Mob Settings
        sprites_folder = os.path.join(resources_folder, "sprites")

        self.hov_size = (150, 150)
        self.hovering_enemy_vel = 4
        self.hov_proj_speed = 10
        self.hov_proj_num = 1

        self.rhl1_path = os.path.join(sprites_folder, "RobotHoverLeft1.png")
        self.rhl2_path = os.path.join(sprites_folder, "RobotHoverLeft2.png")
        self.rhr1_path = os.path.join(sprites_folder, "RobotHoverRight1.png")
        self.rhr2_path = os.path.join(sprites_folder, "RobotHoverRight2.png")
        self.rhA_path = os.path.join(sprites_folder, "RobotHoverLeftAttack.png")
        
        # Custom font
        self.cb2_path = os.path.join(resources_folder, "cb2.ttf")
        
        # Music Settings
        music_folder = os.path.join(resources_folder, "music")
        
        self.titleMusic_path = os.path.join(music_folder, "Title Music.mp3")

        self.music_volume = .05

        # Settings Screen Settings
        self.vol_up_path = os.path.join(resources_folder, "VolUpButton.bmp")
        self.vol_down_path = os.path.join(resources_folder, "VolDownButton.bmp")

        # FPS
        self.clock_tick_interval = 30

        # Player Settings
        self.player_size = (70, 120)
        self.player_speed = 6

        player_folder = os.path.join(sprites_folder, "temp_player")
        self.player_frames = {
            'idle_path': os.path.join(os.path.join(player_folder, "idle"), '1_police_Idle_'),
            'walk_path': os.path.join(os.path.join(player_folder, "walk"), '1_police_Walk_'),
            'file_type': '.png',
            # Saves frame count for each frame list
            'idle_fc': 8,
            'walk_fc': 8
        }

        # Screen Backgrounds
        self.city_background_path = os.path.join(resources_folder, "city_bg.png")
        self.mountains_background_path = os.path.join(resources_folder, "parallax-mountain-bg.png")
        
        # Player Controls
        self.input = {'right': pygame.K_d, 'left': pygame.K_a, 'up': pygame.K_w, 'down': pygame.K_s}
        self.controls_path = os.path.join(resources_folder, "Controls.txt")
        self.initialize_control()
        self.control_button_path = os.path.join(resources_folder, "Button.bmp")
        self.control_flag = False

        self.reset_control_button_path = os.path.join(resources_folder, "ResetButton.bmp")

    # Function Called To Change Player Controls
    def change_control(self, control):
        changed_control = False
        while changed_control is False:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.input[control] = event.key
                    changed_control = True
        self.control_flag = True

    # Function Called To Reset Controls To Default
    def default_settings(self):
        self.control_flag = True
        self.input = {'right': pygame.K_d, 'left': pygame.K_a, 'up': pygame.K_w, 'down': pygame.K_s}
        self.music_volume = .05

    # Function That Reads In Controls From Controls.txt In Resources
    def initialize_control(self):
        file = open(self.controls_path, "r")

        self.input['right'] = int(file.readline())
        self.input['left'] = int(file.readline())
        self.input['up'] = int(file.readline())
        self.input['down'] = int(file.readline())

        file.close()

    # Function Called When Game Is Closed In Order To Save The Current Controls
    def save_controls(self):
        if self.control_flag is False:
            pass
        else:
            file = open(self.controls_path, "w")

            file.write('%d' % self.input['right'])
            file.write("\n")

            file.write('%d' % self.input['left'])
            file.write("\n")

            file.write('%d' % self.input['up'])
            file.write("\n")

            file.write('%d' % self.input['down'])
            file.write("\n")

            file.close()


class GameState(Enum):
    TITLE = 0
    SETTINGS = 1
    ABOUT = 2
    PLAYING = 3
    HIGHSCORES = 4
    QUIT = 5
