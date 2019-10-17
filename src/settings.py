import os
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
        self.bk_color = (39, 184, 184)

        self.num_buttons = 4
        self.title_path = os.path.join(resources_folder, "Title.bmp")
        self.play_path = os.path.join(resources_folder, "PlayButton.bmp")
        self.quit_path = os.path.join(resources_folder, "QuitButton.bmp")
        self.about_path = os.path.join(resources_folder, "AboutButton.bmp")
        self.settings_path = os.path.join(resources_folder, "SettingsButton.bmp")
        self.mainmenu_path = os.path.join(resources_folder, "MainMenuButton.bmp")

        # Screen Backgrounds
        self.title_background_path = os.path.join(resources_folder, "title_bg.png")
        self.city_background_path = os.path.join(resources_folder, "city_bg.png")

        # Mob Settings
        sprites_folder = os.path.join(resources_folder, "sprites")

        self.hov_size = (150, 150)
        self.hovering_enemy_velocity = 2
        self.rhl1_path = os.path.join(sprites_folder, "RobotHoverLeft1.png")
        self.rhl2_path = os.path.join(sprites_folder, "RobotHoverLeft2.png")
        self.rhr1_path = os.path.join(sprites_folder, "RobotHoverRight1.png")
        self.rhr2_path = os.path.join(sprites_folder, "RobotHoverRight2.png")
        
        # Custom font
        self.cb2_path = os.path.join(resources_folder, "cb2.ttf")
        
        # Music Settings
        music_folder = os.path.join(resources_folder, "music")
        
        self.titleMusic_path = os.path.join(music_folder, "Title Music.mp3")


class GameState(Enum):
    TITLE = 0
    SETTINGS = 1
    ABOUT = 2
    PLAYING = 3
    SCORE = 4
    QUIT = 5
