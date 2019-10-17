import pygame

from settings import GameState

class GameScreen(object):
    def __init__(self, screen, game_settings):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.bk_color = game_settings.bk_color
        self.game_settings = game_settings
        
 
    def blitme(self):
        self.screen.fill(self.bk_color)


        text = "BOTTOM TEXT"

        largeText = pygame.font.Font(self.game_settings.cb2_path,80)
        self.textSurface = largeText.render(text, True, (0,0,0))
        self.TextRect = self.textSurface.get_rect()
        self.TextRect.center = ((self.screen_rect.centerx),(self.screen_rect.centery))
        self.screen.blit(self.textSurface, self.TextRect)

    def check_events(self):

        ret_game_state = GameState(3)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                ret_game_state = GameState.QUIT

        return ret_game_state