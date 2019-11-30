import os, pygame
from enum import Enum


class Settings:

    def __init__(self):

        self.resources_folder = os.path.dirname(os.path.realpath("resources"))
        self.resources_folder = os.path.join(self.resources_folder, "resources")

        # Main Display Settings
        self.screen_w = 900
        self.screen_h = 450
        self.game_name = "Cyber Rush"

        # Title Screen Settings
        self.title_background_path = os.path.join(self.resources_folder, "title_bg.png")
        self.bk_color = (39, 184, 184)

        self.num_buttons = 4
        self.title_path = os.path.join(self.resources_folder, "Title.bmp")
        self.play_path = os.path.join(self.resources_folder, "PlayButton.bmp")
        self.quit_path = os.path.join(self.resources_folder, "QuitButton.bmp")
        self.about_path = os.path.join(self.resources_folder, "AboutButton.bmp")
        self.settings_path = os.path.join(self.resources_folder, "SettingsButton.bmp")
        self.mainmenu_path = os.path.join(self.resources_folder, "MainMenuButton.bmp")

        # Mob Settings
        sprites_folder = os.path.join(self.resources_folder, "sprites")

        # Hovering Enemy Settings
        self.hov_size = (105, 144)
        self.hovering_enemy_vel = 4
        self.hov_proj_speed = 15
        self.hov_proj_num = 1

        self.rhl1_path = os.path.join(sprites_folder, "RobotHoverLeft1.png")
        self.rhl2_path = os.path.join(sprites_folder, "RobotHoverLeft2.png")
        self.rhr1_path = os.path.join(sprites_folder, "RobotHoverRight1.png")
        self.rhr2_path = os.path.join(sprites_folder, "RobotHoverRight2.png")
        self.rhA_path = os.path.join(sprites_folder, "RobotHoverLeftAttack.png")

        # Turret Enemy Settings
        self.turret_size = (80, 80)
        self.turret_proj_speed = 15
        self.turret_proj_num = 1

        self.l_turret_path = os.path.join(sprites_folder, "LeftTurret.png")
        self.r_turret_path = os.path.join(sprites_folder, "RightTurret.png")
        
        # Custom font
        self.cb2_path = os.path.join(self.resources_folder, "cb2.ttf")
        
        # Music Settings
        self.music_folder = os.path.join(self.resources_folder, "music")

        self.titleMusic_path = os.path.join(self.music_folder, "Title Music.mp3")

        self.music_volume = .05

        # Settings Screen Settings
        self.vol_up_path = os.path.join(self.resources_folder, "VolUpButton.bmp")
        self.vol_down_path = os.path.join(self.resources_folder, "VolDownButton.bmp")

        # FPS
        self.clock_tick_interval = 30

        # Player Settings
        self.player_size = (102, 102)
        self.player_speed = 6
        self.player_jump = 30
        self.player_skin = 0
        self.player_health = 15

        player_folder = os.path.join(sprites_folder, "player")

        self.player_frames = None
        # self.change_player(self.player_skin)

        self.Player_Preview_1_path = os.path.join(player_folder, "0_preview.png")
        self.Player_Preview_2_path = os.path.join(player_folder, "1_preview.png")

        # Screen Backgrounds
        self.city_background_path = os.path.join(self.resources_folder, "city_bg.png")
        self.mountains_background_path = os.path.join(self.resources_folder, "parallax-mountain-bg.png")
        
        # Player Controls
        self.input = {'right': pygame.K_d, 'left': pygame.K_a, 'up': pygame.K_w, 'down': pygame.K_s}
        self.controls_path = os.path.join(self.resources_folder, "Controls.txt")

        try:
            self.initialize_settings()
        except FileNotFoundError:
            with open(self.controls_path) as file:
                file.close()
            self.default_settings()

        self.control_button_path = os.path.join(self.resources_folder, "Button.bmp")
        self.control_button_path2 = os.path.join(self.resources_folder, "Button2.bmp")
        self.control_flag = False

        self.reset_control_button_path = os.path.join(self.resources_folder, "ResetButton.bmp")

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
        self.player_skin = 1

    # Function That Reads In Controls From Controls.txt In Resources
    def initialize_settings(self):
        file = open(self.controls_path, "r")

        first_line = file.readline()
        if not first_line.strip():
            return

        self.input['right'] = int(first_line)
        self.input['left'] = int(file.readline())
        self.input['up'] = int(file.readline())
        self.input['down'] = int(file.readline())
        self.music_volume = float(file.readline())
        self.player_skin = int(file.readline())
        self.change_player(self.player_skin)

        file.close()

    # Function Called When Game Is Closed In Order To Save The Current Controls
    def save_settings(self):
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

            file.write('%f' % self.music_volume)
            file.write("\n")

            file.write('%d' % self.player_skin)
            file.write("\n")

            file.close()

    def change_player(self, number=None):

        if number is None:
            number = self.player_skin
        elif number == 0 or number == 1:
            self.player_skin = number
        else:
            self.player_skin = number = 0

        self.control_flag = True

        self.resources_folder = os.path.dirname(os.path.realpath("resources"))
        self.resources_folder = os.path.join(self.resources_folder, "resources")
        sprites_folder = os.path.join(self.resources_folder, "sprites")
        player_folder = os.path.join(sprites_folder, "player")

        self.player_frames = {
            'idle_path': os.path.join(os.path.join(player_folder, "idle"), str(number) + '_idle_'),
            'walk_path': os.path.join(os.path.join(player_folder, "walk"), str(number) + '_walk_'),
            'file_type': '.png',
            # Saves frame count for each frame list
            'idle_fc': 3,
            'walk_fc': 4
        }


class GameState(Enum):
    TITLE = 0
    SETTINGS = 1
    ABOUT = 2
    PLAYING = 3
    SCORE = 4
    QUIT = 5
