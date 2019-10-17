import os

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


