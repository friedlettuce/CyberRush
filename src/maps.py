import pygame
from enum import Enum

class MapLoadState(enum):
    MAPSIZE = 0
    MAPNAME = 1
    MAPINFO = 2
    ZONEINFO = 3
    ENEMY = 4
    COLLIDABLE = 5


class Map:

    def __init__(self, screen, game_settings):
        #simple init to get needed objects and initialize a few map variables
        self.screen = screen
        self.game_settings = game_settings
        self.screen_rect = self.screen.get_rect()
        self.sizex = self.sizey = 0
        self.name = ""
        self.spawnpoint = (0,0)

        #function to load level
        #is given path by gamescreen
        def loadMap(self, level_path):
            #to hold which state of maploading we are in
            load_stage = MapLoadState(0)

            #to hold which zone we are currently working on
            cur_zone = (0,0)

            with open(level_path) as f:
                line = f.readline()

                #check if the line isnt a comment, which is denoted by a #
                if line[0] != '#':
                    #first state, get the size of the map
                    if(load_stage == MapLoadStage.MAPSIZE):
                        #size is stored as x,y no spaces
                        pos = line.find(',')
                        self.sizex = line[:pos]
                        self.sizey = line[pos+1:]
                        #create 2d array of zones with size that we just read in
                        self.zones = [[Zone() for j in range(self.sizex)] for i in range(self.sizey)]
                        #set the next state to get map name
                        load_stage = MapLoadStage.MAPNAME

                    #get map name
                    elif(load_stage == MapLoadStage.MAPNAME):
                        self.name = line
                        #set the next state to be general map info
                        load_stage = MapLoadStage.MAPINFO

                    #map loading state for general info
                    #for now this state is just for going into the ZONEINFO state
                    #also setting spawn
                    #may add more later
                    elif(load_stage == MapLoadStage.MAPINFO):
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
                                #set map loading state to zoneinfo
                                load_state = MapLoadingState.ZONEINFO

                            elif(line[:eqpos] == "setspawn"):
                                #set spawn is keyword for setting initial player spawn to certain zone
                                #after the equal sign should be the coords of the zone, as x,y
                                pos = line.find(',')
                                #set new current zone
                                self.spawnpoint[0] = line[eqpos+1:pos]
                                self.spawnpoint[1] = line[pos+1:]

                    elif(load_stage == MapLoadStage.ZONEINFO):
                        pass



class Zone:
    def __init__(self, screen, game_settings):
        pass