import pygame, os


# Generic Enemy Class For Enemies To Utilize
class Enemy(object):
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.movement = 0
        self.vel = 0
        self.end = end
	
    # Function For An Enemy To Move Side To Side On The X Axis
    def move_AlongX(self):
        # If Velocity > 0, Enemy Is Moving To The Right
        if self.vel > 0:
            if self.x < self.pathX[1] + self.vel:
                self.x = self.x + self.vel
            else:
                self.vel = self.vel * -1
                self.x = self.x + self.vel
                self.movement = 0
                
        # If Velocity < 0, Enemy Is Moving To The Left
        elif self.vel < 0:
            if self.x > self.pathX[0] - self.vel:
                self.x = self.x + self.vel
            else:
                self.vel = self.vel * -1
                self.x = self.x + self.vel
                self.movement = 0
    
    #Function For An Enemy To Move Side To Side On The Y Axis
    def move_AlongY(self):
        # If Velocity > 0, Enemy Is Moving Down
        if self.vel > 0:
            if self.y < self.pathY[1] + self.vel:
                self.y = self.y + self.vel
            else:
                self.vel = self.vel * -1
                self.y = self.y + self.vel
                self.movement = 0
                
        # If Velocity < 0, Enemy Is Moving Up
        elif self.vel < 0:
            if self.y > self.pathY[0] - self.vel:
                self.y = self.y + self.vel
            else:
                self.vel = self.vel * -1
                self.y = self.y + self.vel
                self.movement = 0


#Enemy That Will Hover Along X Axis
class HoveringEnemy_X(Enemy):

    def __init__(self, game_settings, x, y, width, height, end):
        super().__init__(x, y, width, height, end)
        self.pathX = [self.x, self.end]
        self.vel = game_settings.hovering_enemy_velocity

        self.moveLeft = [pygame.transform.scale(pygame.image.load(game_settings.rhl1_path), (150,150)),
                    pygame.transform.scale(pygame.image.load(game_settings.rhl2_path), (150,150))]
        self.moveRight = [pygame.transform.scale(pygame.image.load(game_settings.rhr1_path), (150,150)),
                     pygame.transform.scale(pygame.image.load(game_settings.rhr2_path), (150,150))]
    
    def draw(self, screen):
        self.move_AlongX()
        
        if self.movement + 1 == 60:
            self.movement = 0
        
        if self.vel < 0:
            screen.blit(self.moveLeft[self.movement//30],(self.x,self.y))
        elif self.vel > 0:
            screen.blit(self.moveRight[self.movement//30],(self.x,self.y))
        
        self.movement = self.movement + 1

#Enemy That Will Hover Along Y Axis
class HoveringEnemy_Y(Enemy):

    def __init__(self, game_settings, x, y, width, height, end):
        super().__init__(x, y, width, height, end)
        self.pathX = [self.y, self.end]
        self.vel = game_settings.hovering_enemy_velocity

        self.moveLeft = [pygame.image.load(game_settings.rhl1_path),
                    pygame.image.load(game_settings.rhl2_path)]
    
    def draw(self, screen):
        self.move_AlongX()
        
        if self.movement + 1 == 60:
            self.movement = 0
        
        screen.blit(self.moveLeft[self.movement//30],(self.x,self.y))
        self.movement = self.movement + 1