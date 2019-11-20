import os

import pygame


class UI:

    def __init__(self, screen, player):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Sets health bar in UI
        self.health_bar = HealthBar(self.screen, self.screen_rect, player.health)

    def update(self, player):
        self.health_bar.health = player.health

    def blitme(self):
        self.health_bar.blitme()


class HealthBar:

    def __init__(self, screen, screen_rect, player_health):

        self.screen = screen

        self.player_health = player_health
        self.frames = []

        resources_folder = os.path.dirname(os.path.realpath("resources"))
        # resources_folder = os.path.join(resources_folder, "resources")
        hb_folder = os.path.join(os.path.join(resources_folder, "resources"), "health_bar")
        path = os.path.join(hb_folder, "health_bar")

        for frame in range(16):
            cur_f = pygame.transform.scale(pygame.image.load(path + str(frame) + '.png'), (204, 61))
            self.frames.append(cur_f)

        self.frame_rect = self.frames[0].get_rect()
        self.frame_rect.x = screen_rect.bottom
        self.frame_rect.right = screen_rect.right

    def blitme(self):
        self.screen.blit(self.frames[self.player_health], self.frame_rect)
