import pygame
import os
from enum import Enum
import pygame
from mobs import HoveringEnemy
import itertools
from collidable import Collidable


class MapLoadState(Enum):
    MAPSIZE = 0
    MAPNAME = 1
    MAPINFO = 2
    ZONEINFO = 3
    ENEMY = 4
    COLLIDABLE = 5


class Map:

    def __init__(self, screen, game_settings):

        # simple init to get needed objects and initialize a few map variables
        self.screen = screen
        self.game_settings = game_settings
        self.screen_rect = self.screen.get_rect()
        self.sizex = self.sizey = 0

        self.name = ""
        self.zones = None
        self.spawnpoint = [0,0]

        # Map Loading Variables
        self.load_state = MapLoadState(0)
        self.cur_zone = [0, 0]
        self.line = None

        # Enemy attributes
        self.enemy_x = None
        self.enemy_y = None
        self.enemy_endx = None
        self.enemy_endy = None

        # Collidable Attributes
        self.col_x = None
        self.col_y = None
        self.col_w = None
        self.col_h = None
        self.col_color = None

    # function to load level
    # is given path by gamescreen
    def load_map(self, level_path):

        with open(level_path) as f:
            self.line = f.readline()

            # check if the self.line isnt a comment, denoted by '#'
            if self.line[0] != '#':

                if self.load_state == MapLoadState.MAPSIZE:
                    self.map_size()
                elif self.load_state == MapLoadState.MAPNAME:
                    self.map_name()
                elif self.load_state == MapLoadState.MAPINFO:
                    self.map_info()
                elif self.load_state == MapLoadState.ZONEINFO:
                    self.zone_info()
                elif self.load_state == MapLoadState.ENEMY:
                    self.load_enemy()
                elif self.load_state == MapLoadState.COLLIDABLE:
                    self.load_collidable()

        # when done loading map, build connections
        self.build_connections()

    def map_size(self):

        # first state, get the size of the map
        # size is stored as x,y no spaces
        pos = self.line.find(',')
        self.sizex = self.line[:pos]
        self.sizey = self.line[pos + 1:]
        # create 2d array of zones with size that we just read in
        self.zones = [[Zone(self.screen, self.game_settings) for j in range(self.sizex)] for i in range(self.sizey)]
        # set the next state to get map name
        self.load_state = MapLoadState.MAPNAME

    def map_name(self):

        # get map name
        self.name = self.line
        # set the next state to be general map info
        self.load_state = MapLoadState.MAPINFO

    def map_info(self):
        # map loading state for general info
        # for now this state is just for going into the ZONEINFO state
        # also setting spawn
        # may add more later
        # get position of equal sign
        # if its in cur self.line, check for keywords that need that
        # if not, check for keywords without it
        eqpos = self.line.find("=")
        if eqpos == -1:
            # placeholder for if i need keywords in mapinfo state without a =
            pass

        else:
            if self.line[:eqpos] == "editzone":
                # editzone is keyword for editing new zone
                # after the equal sign should be the coords of the zone, as x,y
                pos = self.line.find(',')
                # set new current zone
                self.cur_zone[0] = self.line[eqpos + 1:pos]
                self.cur_zone[1] = self.line[pos + 1:]
                # set used flag to True
                self.zones[self.cur_zone[0]][self.cur_zone[1]].used = True
                # set map loading state to zoneinfo
                self.load_state = MapLoadState.ZONEINFO

            elif self.line[:eqpos] == "setspawn":
                # set spawn is keyword for setting initial player spawn to certain zone
                # after the equal sign should be the coords of the zone, as x,y
                pos = self.line.find(',')
                # set new current zone
                self.spawnpoint[0] = self.line[eqpos + 1:pos]
                self.spawnpoint[1] = self.line[pos + 1:]

    def zone_info(self):

        # get position of equal sign
        # if its in cur self.line, check for keywords that need that
        # if not, check for keywords without it
        eqpos = self.line.find("=")
        if eqpos == -1:
            if self.line == "endzone":
                # go back to mapinfo state
                self.load_state = MapLoadState.MAPINFO
            elif self.line == "addenemy":
                # go to add enemy state
                self.load_state = MapLoadState.ENEMY
            elif self.line == "addcollidable":
                # go to add collidable state
                self.load_state = MapLoadState.COLLIDABLE

        else:
            if self.line[:eqpos] == "setbg":
                # set background of zone
                bgname = self.line[eqpos + 1:]
                bgpath = os.path.join(self.game_settings.resources_folder, bgname)
                self.zones[self.cur_zone[0]][self.cur_zone[1]].set_bg(bgpath)
            elif self.line[:eqpos] == "setmusic":
                # set music of zone
                musicname = self.line[eqpos + 1:]
                musicpath = os.path.join(self.game_settings.music_folder, musicname)
                self.zones[self.cur_zone[0]][self.cur_zone[1]].set_music(musicpath)
            elif self.line[:eqpos] == "setleftspawn":
                # set spawn when coming from left
                pos = self.line.find(',')
                x = self.line[eqpos + 1:pos]
                y = self.line[pos + 1:]
                self.zones[self.cur_zone[0]][self.cur_zone[1]].set_left_spawn(x, y)
            elif self.line[:eqpos] == "setrightspawn":
                # set spawn when coming from right
                pos = self.line.find(',')
                x = self.line[eqpos + 1:pos]
                y = self.line[pos + 1:]
                self.zones[self.cur_zone[0]][self.cur_zone[1]].set_up_spawn(x, y)
            elif self.line[:eqpos] == "setleftspawn":
                # set spawn when coming from up
                pos = self.line.find(',')
                x = self.line[eqpos + 1:pos]
                y = self.line[pos + 1:]
                self.zones[self.cur_zone[0]][self.cur_zone[1]].set_up_spawn(x, y)
            elif self.line[:eqpos] == "setdownspawn":
                # set spawn when coming from down
                pos = self.line.find(',')
                x = self.line[eqpos + 1:pos]
                y = self.line[pos + 1:]
                self.zones[self.cur_zone[0]][self.cur_zone[1]].set_down_spawn(x, y)

    def load_enemy(self):

        # get position of equal sign
        # if its in cur self.line, check for keywords that need that
        # if not, check for keywords without it
        eqpos = self.line.find("=")
        if eqpos == -1:
            if self.line == "endenemy":
                # create enemy object and add to enemies list for current zone
                enemy = HoveringEnemy(self.screen, self.game_settings, self.enemy_x, self.enemy_y,
                                      self.game_settings.hov_size[0],
                                      self.game_settings.hov_size[0], self.enemy_endx, self.enemy_endy)
                # go back to zoneinfo state
                self.load_state = MapLoadState.ZONEINFO

        else:
            if self.line[:eqpos] == "setpos":
                pos = self.line.find(',')
                self.enemy_x = self.line[eqpos + 1:pos]
                self.enemy_y = self.line[pos + 1:]
            elif self.line[:eqpos] == "setendx":
                self.enemy_endx = self.line[eqpos + 1:]
            elif self.line[:eqpos] == "setendy":
                self.enemy_endy = self.line[eqpos + 1:]

    def load_collidable(self):

        # get position of equal sign
        # if its in cur self.line, check for keywords that need that
        # if not, check for keywords without it
        eqpos = self.line.find("=")
        if eqpos == -1:
            if self.line == "endcollidable":
                # create rect for collidable
                r = pygame.Rect(self.col_x, self.col_y, self.col_w, self.col_h)
                # create color tuple
                color = (self.col_color[0:3], self.col_color[3:6], self.col_color[6:])
                # create collidable object and add to collidables list for current zone
                c = Collidable(self.screen, r, color)
                self.zones[self.cur_zone[0]][self.cur_zone[1]].add_collidable(c)
                # go back to zoneinfo state
                self.load_state = MapLoadState.ZONEINFO

        else:
            if self.line[:eqpos] == "setpos":
                pos = self.line.find(',')
                self.col_x = self.line[eqpos + 1:pos]
                self.col_y = self.line[pos + 1:]
            elif self.line[:eqpos] == "setdims":
                pos = self.line.find(',')
                self.col_w = self.line[eqpos + 1:pos]
                self.col_h = self.line[pos + 1:]
            elif self.line[:eqpos] == "setcolor":
                self.col_color = self.line[eqpos + 1:]

    def build_connections(self):

        # this function builds the connections between the zones of the maps
        # sets whether going to the edge of a zone should take the player
        # to the next zone or not

        for x, y in itertools.product(range(self.sizex), range(self.sizey)):
            if self.zones[x][y].used:
                # only check zones which are used
                if y > 0:
                    # if y>0, check the zone above us, which is y-1
                    if self.zones[x][y-1]:
                        # if this zone is used, set up zone used flag in current zone to true
                        self.zones[x][y].up_used = True
                if y < self.sizey-1:
                    # if y<max size, check the zone below us, which is y+1
                    if self.zones[x][y+1]:
                        # if this zone is used, set up zone used flag in current zone to true
                        self.zones[x][y].down_used = True
                if x > 0:
                    # if y>0, check the zone to our left, which is x-1
                    if self.zones[x-1][y]:
                        # if this zone is used, set left zone used flag in current zone to true
                        self.zones[x][y].left_used = True
                if x < self.sizex-1:
                    # if x<max size, check the zone to our right, which is x+1
                    if self.zones[x+1][y]:
                        # if this zone is used, set right zone used flag in current zone to true
                        self.zones[x][y].right_used = True


class Zone:

    def __init__(self, screen, game_settings):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.game_settings = game_settings
        self.music = "none"

        # variable to hold if this zone is used in the map
        self.used = False

        # variables to hold if the zones around this one are used
        # used for transfering between zones
        self.left_used = False
        self.right_used = False
        self.up_used = False
        self.down_used = False

        self.bg = None
        self.bg_rect = self.bg.get_rect()

        self.leftspawn = None
        self.upspawn = None
        self.downspawn = None
        self.rightspawn = None

        self.enemies = None
        self.collidables = None

    def set_left_spawn(self, x, y):
        self.leftspawn[0] = x
        self.leftspawn[1] = y

    def set_up_spawn(self, x, y):
        self.upspawn[0] = x
        self.upspawn[1] = y

    def set_down_spawn(self, x, y):
        self.downspawn[0] = x
        self.downspawn[1] = y

    def set_right_spawn(self, x, y):
        self.rightspawn[0] = x
        self.rightspawn[1] = y

    def add_enemy(self, e):
        self.enemies.apend(e)

    def add_colliadable(self, c):
        self.collidables.apend(c)

    def set_bg(self, bg):
        self.bg = pygame.image.load(bg)
        self.bg = pygame.transform.scale(
            self.bg, (self.game_settings.screen_w, self.game_settings.screen_h))

        self.bg_rect.centerx = self.screen_rect.centerx
        self.bg_rect.centery = self.screen_rect.centery

    def set_music(self, m):
        self.music = m

