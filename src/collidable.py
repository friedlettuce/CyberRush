from pygame import draw, rect


class Collidable:

    def __init__(self, screen, obj_rect, color):

        self.screen = screen
        self.rect = obj_rect
        self.color = color

    def check_collision(self, obj_rect):

        if self.rect.colliderect(obj_rect):
            return

        # Checks left collisions
        top_left = obj_rect.collidepoint(self.rect.topleft)
        mid_left = obj_rect.collidepoint(self.rect.midleft)
        bottom_left = obj_rect.collidepoint(self.rect.bottomleft)

        # Checks right collisions
        top_right = obj_rect.collidepoint(self.rect.topright)
        mid_right = obj_rect.collidepoint(self.rect.midright)
        bottom_right = obj_rect.collidepoint(self.rect.bottomright)

        # Checks top and bottom collisions
        top_mid = obj_rect.collidepoint(self.rect.midtop)
        bottom_mid = obj_rect.collidepoint(self.rect.midbottom)

        if top_left:
            obj.collide_tleft()
        elif mid_left:
            obj.collide_mleft()
        elif bottom_left:
            obj.collide_bleft()
        elif top_right:
            obj.collide_tright()
        elif mid_right:
            obj.collide_mright()
        elif bottom_right:
            obj.collide_bright()
        elif top_mid:
            obj.collide_tmid()
        elif bottom_mid:
            obj.collide_bmid()

    def blitme(self):
        draw.rect(self.screen, self.color, self.rect)
