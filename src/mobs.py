import pygame, os


# Generic Enemy Class For Enemies To Utilize
class Enemy(object):
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.movement = 0
        self.end = end

        self.hitbox = 0
        self.hitbox2 = 0
        self.vel = 0

    # Function For An Enemy To Move Side To Side On The X Axis
    def moving_x(self):
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
    
    # Function For An Enemy To Move Side To Side On The Y Axis
    def moving_y(self):
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


# Enemy That Will Hover Along X Axis
class HoveringEnemyX(Enemy):

    def __init__(self, game_settings, x, y, width, height, end):
        super().__init__(x, y, width, height, end)
        self.pathX = [self.x, self.end]
        self.vel = game_settings.hovering_enemy_velocity

        self.moveLeft = [pygame.transform.scale(pygame.image.load(game_settings.rhl1_path), game_settings.hov_size),
                    pygame.transform.scale(pygame.image.load(game_settings.rhl2_path), game_settings.hov_size)]
        self.moveRight = [pygame.transform.scale(pygame.image.load(game_settings.rhr1_path), game_settings.hov_size),
                     pygame.transform.scale(pygame.image.load(game_settings.rhr2_path), game_settings.hov_size)]

    def blitme(self, screen):
        self.moving_x()

        if self.movement + 1 == 40:
            self.movement = 0
        
        if self.vel < 0:
            screen.blit(self.moveLeft[self.movement//20],(self.x, self.y))
            self.hitbox = (self.x + 50, self.y + 25, 45, 110)
            self.hitbox2 = (self.x + 40, self.y + 25, 80, 35)
        elif self.vel > 0:
            screen.blit(self.moveRight[self.movement//20],(self.x, self.y))
            self.hitbox = (self.x + 50, self.y + 25, 45, 110)
            self.hitbox2 = (self.x + 30, self.y + 25, 80, 35)
        
        self.movement = self.movement + 1
        
        #self.draw_hitbox(screen)
       
    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox2, 2)


# Enemy That Will Hover Along Y Axis
class HoveringEnemyY(Enemy):

    def __init__(self, game_settings, x, y, width, height, end):
        super().__init__(x, y, width, height, end)
        self.pathY = [self.y, self.end]
        self.vel = game_settings.hovering_enemy_velocity

        self.moveLeft = [pygame.transform.scale(pygame.image.load(game_settings.rhl1_path), game_settings.hov_size),
                    pygame.transform.scale(pygame.image.load(game_settings.rhl2_path), game_settings.hov_size)]
    
        self.projectiles = []
        
    def blitme(self, screen):
        self.moving_y()
        
        if self.movement + 1 == 60:
            self.movement = 0
        
        screen.blit(self.moveLeft[self.movement//30], (self.x, self.y))
        self.movement = self.movement + 1
        
        if not self.y > self.pathY[0] - self.vel:
            self.projectiles.append(Projectile_X(self.x, self.y + 40, 25, 25))
        elif not self.y < self.pathY[1] + self.vel and len(self.projectiles) < 1:
            self.projectiles.append(Projectile_X(self.x, self.y + 20, 25, 25))
        
        for projectile in self.projectiles:
                if projectile.x < self.x - 250:
                    self.projectiles.pop(self.projectiles.index(projectile))
                else:
                    projectile.move()
                    #projectile.blitme(screen)
        
        self.hitbox = (self.x + 50, self.y + 25, 45, 110)
        self.hitbox2 = (self.x + 40, self.y + 25, 80, 35)
        
        #self.draw_hitbox(screen)
    
    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox2, 2)


class Projectile_X(object):
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def move(self):
        self.x = self.x - 5
        
    def blitme(self, screen):
        pygame.draw.rect(screen, (0,255,0), (self.x, self.y, self.width, self.height))