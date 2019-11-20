from pygame import draw, rect


class Collidable:

    def __init__(self, screen, obj_rect, color):

        self.screen = screen
        self.rect = obj_rect
        self.color = color
        #flag for if object moves
        self.moving = False

    def check_collision(self, obj_rect):
        if self.rect.colliderect(obj_rect):
            return True

        return False

    def blitme(self):
        draw.rect(self.screen, self.color, self.rect)
