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
        self.spawnpoint = [0,0]

    #function to load level
    #is given path by gamescreen
    def loadMap(self, level_path):
        #to hold which state of maploading we are in
        load_state = MapLoadState(0)

        #to hold which zone we are currently working on
        cur_zone = [0,0]

        with open(level_path) as f:
            line = f.readline()

            #check if the line isnt a comment, which is denoted by a #
            if line[0] != '#':
                #first state, get the size of the map
                if(load_state == MapLoadState.MAPSIZE):
                    #size is stored as x,y no spaces
                    pos = line.find(',')
                    self.sizex = line[:pos]
                    self.sizey = line[pos+1:]
                    #create 2d array of zones with size that we just read in
                    self.zones = [[Zone(self.screen, self.game_settings) for j in range(self.sizex)] for i in range(self.sizey)]
                    #set the next state to get map name
                    load_state = MapLoadState.MAPNAME

                #get map name
                elif(load_state == MapLoadState.MAPNAME):
                    self.name = line
                    #set the next state to be general map info
                    load_state = MapLoadState.MAPINFO

                #map loading state for general info
                #for now this state is just for going into the ZONEINFO state
                #also setting spawn
                #may add more later
                elif(load_state == MapLoadState.MAPINFO):
                    #get position of equal sign
                    #if its in cur line, check for keywords that need that
                    #if not, check for keywords without it
                    eqpos = line.find("=")
                    if(eqpos == -1):
                        #placeholder for if i need keywords in mapinfo state without a =
                        pass

                    else:
                        if(line[:eqpos] == "editzone"):
                            #editzone is keyword for editing new zone
                            #after the equal sign should be the coords of the zone, as x,y
                            pos = line.find(',')
                            #set new current zone
                            cur_zone[0] = line[eqpos+1:pos]
                            cur_zone[1] = line[pos+1:]
                            #set used flag to True
                            self.zones[cur_zone[0]][cur_zone[1]].used = true
                            #set map loading state to zoneinfo
                            load_state = MapLoadState.ZONEINFO

                        elif(line[:eqpos] == "setspawn"):
                            #set spawn is keyword for setting initial player spawn to certain zone
                            #after the equal sign should be the coords of the zone, as x,y
                            pos = line.find(',')
                            #set new current zone
                            self.spawnpoint[0] = line[eqpos+1:pos]
                            self.spawnpoint[1] = line[pos+1:]

                elif(load_state == MapLoadState.ZONEINFO):
                    #get position of equal sign
                    #if its in cur line, check for keywords that need that
                    #if not, check for keywords without it
                    eqpos = line.find("=")
                    if(eqpos == -1):
                        if(line == "endzone"):
                            #go back to mapinfo state
                            load_state = MapLoadState.MAPINFO
                        elif(line == "addenemy"):
                            #go to add enemy state
                            load_state = MapLoadState.ENEMY
                        elif(line == "addcollidable"):
                            #go to add collidable state
                            load_state = MapLoadState.COLLIDABLE

                    else:
                        if(line[:eqpos] == "setbg"):
                            #set background of zone
                            bgname = line[eqpos+1:]
                            bgpath = os.path.join(self.gamesettings.resources_folder, bgname)
                            self.zones[curzone[0]][curzone[1]].set_bg(bgpath)
                        elif(line[:eqpos] == "setmusic"):
                            #set music of zone
                            musicname = line[eqpos+1:]
                            musicpath = os.path.join(self.game_settings.music_folder, musicname)
                            self.zones[curzone[0]][curzone[1]].set_music(musicpath)
                        elif(line[:eqpos] == "setleftspawn"):
                            #set spawn when coming from left
                            pos = line.find(',')
                            x = line[eqpos+1:pos]
                            y = line[pos+1:]
                            self.zones[curzone[0]][curzone[1]].set_left_spawn(x,y)
                        elif(line[:eqpos] == "setrightspawn"):
                            #set spawn when coming from right
                            pos = line.find(',')
                            x = line[eqpos+1:pos]
                            y = line[pos+1:]
                            self.zones[curzone[0]][curzone[1]].set_up_spawn(x,y)
                        elif(line[:eqpos] == "setleftspawn"):
                            #set spawn when coming from up
                            pos = line.find(',')
                            x = line[eqpos+1:pos]
                            y = line[pos+1:]
                            self.zones[curzone[0]][curzone[1]].set_up_spawn(x,y)
                        elif(line[:eqpos] == "setdownspawn"):
                            #set spawn when coming from down
                            pos = line.find(',')
                            x = line[eqpos+1:pos]
                            y = line[pos+1:]
                            self.zones[curzone[0]][curzone[1]].set_down_spawn(x,y)

                elif(load_state == MapLoadState.ENEMY):
                    #get position of equal sign
                    #if its in cur line, check for keywords that need that
                    #if not, check for keywords without it
                    eqpos = line.find("=")
                    if(eqpos == -1):
                        if(line == "endenemy"):
                            #create enemy object and add to enemies list for current zone
                            enemy = HoveringEnemy(self.screen, self.game_settings, self.enemyx, self.enemyy, self.game_settings.hov_size[0], 
                                                    self.game_settings.hov_size[0], self.enemyendx, self.enemyendy)
                            #go back to zoneinfo state
                            load_state = MapLoadState.ZONEINFO

                    else:
                        if(line[:eqpos] == "setpos"):
                            pos = line.find(',')
                            self.enemyx = line[eqpos+1:pos]
                            self.enemyy = line[pos+1:]
                        elif(line[:eqpos] == "setendx"):
                            self.enemyendx = line[eqpos+1:]
                        elif(line[:eqpos] == "setendy"):
                            self.enemyendy = line[eqpos+1:]

                elif(load_state == MapLoadState.Collidable):
                    #get position of equal sign
                    #if its in cur line, check for keywords that need that
                    #if not, check for keywords without it
                    eqpos = line.find("=")
                    if(eqpos == -1):
                        if(line == "endcollidable"):
                            #create rect for collidable
                            r = Rect(self.colx, self.coly, self.colw, self.colh)
                            #create color tuple 
                            color = (self.colcolor[0:3], self.colcolor[3:6], self.colcolor[6:])
                            #create collidable object and add to collidables list for current zone
                            c = Collidable(self.screen, r, color)
                            self.zones[curzone[0]][curzone[1]].add_collidable(c)
                            #go back to zoneinfo state
                            load_state = MapLoadState.ZONEINFO
                    
                    else:
                        if(line[:eqpos] == "setpos"):
                            pos = line.find(',')
                            self.colx = line[eqpos+1:pos]
                            self.coly = line[pos+1:]
                        elif(line[:eqpos] == "setdims"):
                            pos = line.find(',')
                            self.colw = line[eqpos+1:pos]
                            self.colh = line[pos+1:]
                        elif(line[:eqpos] == "setcolor"):
                            self.colcolor = line[eqpos+1:]

        #when done loading map, build connections
        build_connections()


    def build_connections(self):
        #this function builds the connections between the zones of the maps
        #sets whether going to the edge of a zone should take the player
        #to the next zone or not
        for x,y in itertools.product(range(self.sizex), range(self.sizey)):
            if(self.zones[x][y].used):
                #only check zones which are used
                if(y>0):
                    #if y>0, check the zone above us, which is y-1
                    if(self.zones[x][y-1]):
                        #if this zone is used, set up zone used flag in current zone to true
                        self.zones[x][y].up_used = true
                if(y<self.sizey-1):
                    #if y<max size, check the zone below us, which is y+1
                    if(self.zones[x][y+1]):
                        #if this zone is used, set up zone used flag in current zone to true
                        self.zones[x][y].down_used = true
                if(x>0):
                    #if y>0, check the zone to our left, which is x-1
                    if(self.zones[x-1][y]):
                        #if this zone is used, set left zone used flag in current zone to true
                        self.zones[x][y].left_used = true
                if(x<self.sizex-1):
                    #if x<max size, check the zone to our right, which is x+1
                    if(self.zones[x+1][y]):
                        #if this zone is used, set right zone used flag in current zone to true
                        self.zones[x][y].right_used = true

class Zone:

    def __init__(self, screen, game_settings):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.game_settings = game_settings
        self.music = "none"
        #variable to hold if this zone is used in the map
        self.used = false
        #variables to hold if the zones around this one are used
        #used for transfering between zones
        self.left_used = false
        self.right_used = false
        self.up_used = false
        self.down_used = false

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

