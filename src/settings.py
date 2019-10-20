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

        self.num_buttons = 4
        self.title_path = os.path.join(resources_folder, "Title.bmp")
        self.play_path = os.path.join(resources_folder, "PlayButton.bmp")
        self.quit_path = os.path.join(resources_folder, "QuitButton.bmp")
        self.about_path = os.path.join(resources_folder, "AboutButton.bmp")
        self.settings_path = os.path.join(resources_folder, "SettingsButton.bmp")
        self.mainmenu_path = os.path.join(resources_folder, "MainMenuButton.bmp")

        # Mob Settings
        sprites_folder = os.path.join(resources_folder, "sprites")

        self.hov_size = (150, 150)
        self.hovering_enemy_vel = 2
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
        self.clock_tick_interval = 60

        # Player Settings
        self.player_size = (70, 120)
        self.player_speed = 3

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
        self.input = {'right': pygame.K_RIGHT, 'left': pygame.K_LEFT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}


class GameState(Enum):
    TITLE = 0
    SETTINGS = 1
    ABOUT = 2
    PLAYING = 3
    SCORE = 4
    QUIT = 5
