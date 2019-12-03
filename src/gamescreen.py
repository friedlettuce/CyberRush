from os import path
import pygame

from settings import GameState
from player import Player
from maps import Map
from ui import UI


class GameScreen(object):

    def __init__(self, screen, game_settings):

        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.game_settings = game_settings
        self.input = game_settings.input

        # Map
        level_path = path.dirname(path.realpath("resources"))
        self.map = Map(self.screen, self.game_settings, path.join(level_path, 'level_02.txt'))
        self.cur_zone_coords = self.map.spawnpoint
        self.cur_zone = self.map.zones[self.cur_zone_coords[0]][self.cur_zone_coords[1]]
        self.spawn = self.map.zones[self.map.spawnpoint[0]][self.map.spawnpoint[1]]
        self.player = Player(self.screen, game_settings, self.spawn.leftspawn[0], self.spawn.leftspawn[1])
        self.ui = UI(self.screen, self.player)

        pygame.mixer.set_num_channels(8)

    def screen_start(self):
        pygame.mixer.music.stop()

        # Sets player keys and spawn
        self.input = self.game_settings.input

        self.player.clear_frames()
        self.player.load_frames(self.game_settings.player_frames)

    def check_collisions(self, collidable):

        for enemy in self.cur_zone.enemies:

            # Deals with projectiles colldining into collidables
            for projcollide in self.cur_zone.collidables:
                enemy.collide_projectiles(projcollide)
                self.player.collide_projectiles(projcollide)

            # Deals damage to player when collides with projectiles
            damage_player = enemy.collide_projectiles(self.player)
            damage_enemy = self.player.collide_projectiles(enemy)
            if self.player.hitting and self.player.frame_count > 2 and not self.player.hit:
                damage_enemy += self.player.check_collision(enemy.get_rect())
                self.player.hit = True

            if damage_player > 0 or damage_enemy > 0:
                pygame.mixer.Sound.play(self.game_settings.player_damage_sound)

            if damage_player > self.player.health:
                self.player.health = 0
            else:
                self.player.health -= damage_player
            if damage_enemy > enemy.health:
                enemy.health = 0
            else:
                enemy.health -= damage_enemy

        while self.cur_zone.collision_by_x(self.player, collidable):
            if collidable.moving and self.player.vel_x == 0:
                # if the player is colliding with a moving object
                # and the player isnt moving, then move the player the same direction
                # the object they are colliding with is moving
                vel = 1
                if not collidable.facing_right:
                    vel = -1
            else:
                # otherwise, move them normally to fix collision
                # if x is causing collision, move x back by 1
                vel = 1
                if self.player.facing_right:
                    # if moving left, vel is negative
                    vel = -1

            self.player.move_by_amount(vel, 0)
        
        yfixed = False
        while self.cur_zone.collision_by_y(self.player, collidable):
            yfixed = True
            if collidable.moving and (self.player.vel_y == 0 or self.player.vel_y == -1):
                # if the player is colliding with a moving object
                # and the player isnt moving, then move the player the same direction
                # the object they are colliding with is moving
                vel = 1
                if collidable.vel_y <= 0:
                    vel = -1
            else:
                vel = 1
                if self.player.vel_y < 0:
                    vel = -1

            # if y is causing collision, move y back by 1
            self.player.move_by_amount(0, vel)

        moving_collidable = None
        if yfixed and collidable.moving:
            # if the player is colliding with a moving object
            # then return the collidable to do things with later
            moving_collidable = collidable
        return yfixed, moving_collidable

    def update(self):

        self.player.move()
        self.cur_zone.update_enemies(self.player)

        yfixed = False
        moving_collidable = None

        for collidable in self.cur_zone.collidables:
            ret_vals = self.check_collisions(collidable)
            if ret_vals[0]:
                yfixed = True
            if ret_vals[1] is not None:
                moving_collidable = ret_vals[1]

        for collidable in self.cur_zone.enemies:

            ret_vals = self.check_collisions(collidable)
            if ret_vals[0]:
                yfixed = True
            if ret_vals[1] is not None:
                moving_collidable = ret_vals[1]

        # reset player jump
        if yfixed:
            self.player.land()
            if moving_collidable is not None and self.player.y > moving_collidable.y and self.player.vel_y < 0:
                # if we collide with an object moving downwards while we are under it, dont reset player vel_y
                # this stops us from "sticking" to the bottom of the object
                pass
            else:
                self.player.vel_y = 0
            
        if moving_collidable is not None and moving_collidable.vel_y > 0 and self.player.y < moving_collidable.y:
            # if we are moving down on top of a collidable
            # then snap the player to the top of the collidable
            # and match vel_y
            # also add collidables vel_x, so collidable carries player
            self.player.get_rect().bottom = moving_collidable.get_rect().top
            self.player.vel_y = -moving_collidable.vel_y
            self.player.x += moving_collidable.vel_x

        if moving_collidable is not None and moving_collidable.vel_y <= 0 and self.player.y < moving_collidable.y:
            # if we are moving up on top of a collidable
            # the add collidables vel_x, so collidable carries player
            self.player.x += moving_collidable.vel_x

        self.cur_zone_coords, dir = self.cur_zone.check_oob(self.player, self.cur_zone_coords)
        self.cur_zone = self.map.zones[self.cur_zone_coords[0]][self.cur_zone_coords[1]]
        if dir == "right":
            #we moved to the right
            self.player.x = self.cur_zone.leftspawn[0]
            self.player.y = self.cur_zone.leftspawn[1]
        if dir == "left":
            #we moved to the left
            self.player.x = self.cur_zone.rightspawn[0]
            self.player.y = self.cur_zone.rightspawn[1]
        if dir == "up":
            #we moved up
            self.player.x = self.cur_zone.downspawn[0]
            self.player.y = self.cur_zone.downspawn[1]
        if dir == "down":
            #we moved down
            self.player.x = self.cur_zone.upspawn[0]
            self.player.y = self.cur_zone.upspawn[1]
        self.ui.update(self.player)

    def check_events(self):

        if self.player.health <= 0:
            return GameState(5)     # Go to leaderboard when integrated
        ret_game_state = GameState(3)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                ret_game_state = GameState.QUIT

            elif event.type == pygame.KEYDOWN:

                if event.key == self.input['up']:
                    self.player.jump()

                if event.key == self.input['left']:
                    self.player.set_movement(False)

                if event.key == self.input['right']:
                    self.player.set_movement(True)

                if event.key == self.input['melee']:
                    self.player.melee()
                elif event.key == self.input['shoot']:
                    self.player.shoot()

            elif event.type == pygame.KEYUP:

                if event.key == self.input['left']:
                    self.player.set_movement(False, False)

                if event.key == self.input['right']:
                    self.player.set_movement(True, False)

        return ret_game_state

    def screen_end(self):
        pass

    def blitme(self):

        self.cur_zone.blitme()
        self.ui.blitme()
        # pygame.draw.rect(self.screen,(111,111,111),self.player.get_rect())
        self.player.blitme()
