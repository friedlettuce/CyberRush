import sys
import pygame


def check_events():

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        # elif event.type == pygame.KEYDOWN:
            # Update player/game state

        # elif event.type == pygame.KEYUP:
            # Update player/game state


def update_screen():
    # Blit/Update/Manage game display

    pygame.display.flip()
