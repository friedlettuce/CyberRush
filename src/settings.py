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
        self.level = 'level_01.txt'

        # Title Screen Settings
        self.title_background_path = os.path.join(self.resources_folder, "title_bg.png")
        self.bk_color = (39, 184, 184)

        self.num_buttons = 5  # Changed this from 4 to 5
        self.title_path = os.path.join(self.resources_folder, "Title.bmp")
        self.play_path = os.path.join(self.resources_folder, "PlayButton.bmp")
        self.quit_path = os.path.join(self.resources_folder, "QuitButton.bmp")
        self.about_path = os.path.join(self.resources_folder, "AboutButton.bmp")
        self.highscores_path = os.path.join(self.resources_folder,
                                            "HighScoresButton.bmp")  # Added button to go to highscores screen
        self.placeholder_path = os.path.join(self.resources_folder,
                                             "PlaceholdersButton.bmp")  # Added button to add placeholders in highscores
        self.settings_path = os.path.join(self.resources_folder, "SettingsButton.bmp")
        self.mainmenu_path = os.path.join(self.resources_folder, "MainMenuButton.bmp")
        self.credits_path = os.path.join(self.resources_folder, "Credits.bmp")


        # Mob Settings
        sprites_folder = os.path.join(self.resources_folder, "sprites")

        # Hovering Enemy Settings
        self.hov_size = (87, 120)
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

        # Spaceship Enemy Boss Settings
        self.ship_path = os.path.join(sprites_folder, "spaceships")
        self.ship = {}
        self.ship_proj_speed = 10
        self.ship_proj_num = 1
        
        # Custom font
        self.cb2_path = os.path.join(self.resources_folder, "cb2.ttf")
        
        # Music Settings
        self.music_folder = os.path.join(self.resources_folder, "music")

        self.titleMusic_path = os.path.join(self.music_folder, "Title Music.mp3")


        self.music_volume = .05

        # Sound Effect Settings
        self.sound_effect_folder = os.path.join(self.resources_folder, "sound_effects")

        self.player_damage_sound = pygame.mixer.Sound(os.path.join(self.sound_effect_folder, "Player_Damage.wav"))
        self.player_damage_sound.set_volume(self.music_volume * 200)

        self.player_jump_sound = pygame.mixer.Sound(os.path.join(self.sound_effect_folder, "Jump.wav"))
        self.player_jump_sound.set_volume(self.music_volume * 2)

        self.button_click_sound = pygame.mixer.Sound(os.path.join(self.sound_effect_folder, "Button.wav"))

        self.button_click_sound_2 = pygame.mixer.Sound(os.path.join(self.sound_effect_folder, "Settings_Button.wav"))

        self.enemy_attack_sound = pygame.mixer.Sound(os.path.join(self.sound_effect_folder, "Enemy_Attack.wav"))

        self.enemy_death_sound = pygame.mixer.Sound(os.path.join(self.sound_effect_folder, "Explosion.wav"))

        self.player_ranged_sound = pygame.mixer.Sound(os.path.join(self.sound_effect_folder, "Player_Attack.wav"))

        # Settings Screen Settings
        self.vol_up_path = os.path.join(self.resources_folder, "VolUpButton.bmp")
        self.vol_down_path = os.path.join(self.resources_folder, "VolDownButton.bmp")

        # FPS
        self.clock_tick_interval = 30

        # Player Settings

        self.player_size = (56, 85)
        self.player_speed = 6
        self.player_jump = 30
        self.player_skin = 0
        self.player_projectile = 0
        self.player_health = 15
        self.player_counter_divisor = 5
        self.player_counter_max = 16


        player_folder = os.path.join(sprites_folder, "player")

        self.player_frames = None

        self.Player_Preview_1_path = os.path.join(player_folder, "0_preview.png")
        self.Player_Preview_2_path = os.path.join(player_folder, "1_preview.png")

        self.Projectile_Preview_1_path = os.path.join(player_folder, "0_preview2.png")
        self.Projectile_Preview_2_path = os.path.join(player_folder, "1_preview2.png")

        # Screen Backgrounds

        self.city_background_path = os.path.join(self.resources_folder, "city_bg.png")
        self.mountains_background_path = os.path.join(self.resources_folder, "parallax-mountain-bg.png")
        
        # Player Controls
        self.input = {'right': pygame.K_d, 'left': pygame.K_a, 'up': pygame.K_w, 'shoot': pygame.K_s,
                      'melee': pygame.K_e, 'roll': pygame.K_LSHIFT}
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

        self.input = {'right': pygame.K_d, 'left': pygame.K_a, 'up': pygame.K_w, 'shoot': pygame.K_s,
                      'melee': pygame.K_e, 'roll': pygame.K_LSHIFT}
        self.music_volume = .05
        pygame.mixer.music.set_volume(self.music_volume)
        self.player_skin = 0
        self.player_projectile = 0

    # Function That Reads In Controls From Controls.txt In Resources
    def initialize_settings(self):
        file = open(self.controls_path, "r")

        first_line = file.readline()
        if not first_line.strip():
            return

        self.input['right'] = int(first_line)
        self.input['left'] = int(file.readline())
        self.input['up'] = int(file.readline())
        self.input['shoot'] = int(file.readline())
        self.input['melee'] = int(file.readline())
        self.input['roll'] = int(file.readline())
        self.music_volume = float(file.readline())
        self.player_skin = int(file.readline())
        self.player_projectile = int(file.readline())
        self.change_player(self.player_skin, self.player_projectile)


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


            file.write('%d' % self.input['shoot'])
            file.write("\n")

            file.write('%d' % self.input['melee'])
            file.write("\n")

            file.write('%d' % self.input['roll'])
            file.write("\n")

            file.write('%f' % self.music_volume)
            file.write("\n")

            file.write('%d' % self.player_skin)
            file.write("\n")

            file.write('%d' % self.player_projectile)
            file.write("\n")

            file.close()

    def change_player(self, number=None, number2=None):

        if number is None:
            number = self.player_skin
        elif number == 0 or number == 1:
            self.player_skin = number
        else:
            self.player_skin = number = 0

        if number2 is None:
            number2 = self.player_projectile
        elif number2 == 0 or number2 == 1:
            self.player_projectile = number2
        else:
            self.player_projectile = number2 = 0

        self.control_flag = True

        self.resources_folder = os.path.dirname(os.path.realpath("resources"))
        self.resources_folder = os.path.join(self.resources_folder, "resources")
        sprites_folder = os.path.join(self.resources_folder, "sprites")
        player_folder = os.path.join(sprites_folder, "player")

        self.player_frames = {
            'idle': {
                'path': os.path.join(os.path.join(player_folder, "idle"), str(number) + '_idle_'),
                'fc': 3
            },
            'walking': {
                'path': os.path.join(os.path.join(player_folder, "walk"), str(number) + '_walk_'),
                'fc': 4
            },
            'jumping': {
                'path': os.path.join(os.path.join(player_folder, "jump"), str(number) + '_jumping_'),
                'fc': 8
            },
            'melee': {
                'path': os.path.join(os.path.join(os.path.join(
                    player_folder, "attack"), "melee"), str(number) + '_melee_0_'),
                'fc': 5
            },
            'shooting': {
                'path': os.path.join(os.path.join(os.path.join(
                    player_folder, "attack"), "projectile"), str(number) + '_shoot_'),
                'fc': 5
            },
            'projectile': {
                'path': os.path.join(os.path.join(os.path.join(
                    player_folder, "attack"), "projectile"), str(number2) + '_projectile_'),
                'fc': 4,
                'size': (33, 11)
            },
            'roll': {
                'path': os.path.join(os.path.join(
                    player_folder, "extras"), str(number) + '_roll_'),
                'fc': 7,
            },
            'file_type': '.png'
        }

    def load_ship(self, number):
        if number < 0 or number > 6:
            number = 3
        ship_path = os.path.join(self.ship_path, 'Ship' + str(number))
        parts_path = os.path.join(ship_path, 'Parts')
        parts_list = os.path.join(parts_path, 'list.txt')

        parts = []
        path = None
        size = None
        offset = None
        part_priority = None

        with open(parts_list, 'r') as pl:

            survivable = int(pl.readline())

            for line in pl:
                line = line.split()
                # Checks list of parts for file, offset, and size by line
                for word in line:

                    if path is None:
                        path = word
                    elif offset is None:
                        # Splits at 4 to check for sign
                        x = int(word[:4])
                        y = int(word[4:])
                        offset = (x, y)
                    elif part_priority is None:
                        part_priority = int(word)
                    elif size is None:
                        # Splits at 4 to check for sign
                        x = int(word[:3])
                        y = int(word[3:])
                        size = (x, y)

                parts.append({
                    'path': os.path.join(parts_path, path),
                    'offset': offset,
                    'priority': part_priority,
                    'size': size
                })
                path = size = offset = part_priority = None

        self.ship = {
            'parts': parts,
            'parts_file': '.png',
            'shots': os.path.join(os.path.join(ship_path, 'Shot' + str(number)), 'shot' + str(number) + '_'),
            'shots_file': '.png',
            'shots_fc': 4,
            'width': 172,
            'height': 78,
            'vel_x': 5,
            'vel_y': 3,
            'survivable': survivable
        }


class GameState(Enum):
    TITLE = 0
    SETTINGS = 1
    ABOUT = 2
    PLAYING = 3
    HIGHSCORES = 4
    QUIT = 5
