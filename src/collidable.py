import pygame


class Collidable:

    def __init__(self, screen, rect, color):

        self.screen = screen
        self.rect = rect
        self.color = color

    def check_collision(self, obj):

        if self.rect.colliderect(obj.get_rect()):
            return True
        else:
            return False

    def blitme(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
