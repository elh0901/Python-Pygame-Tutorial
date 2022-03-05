import pygame
from sprites import *
import maps
from sounds import *
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.width, self.height = TILESIZE, TILESIZE

        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        Player_animation(self)

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'



    def collide_enemy(self):
        global LIVES
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            if self.facing == "right":
                for sprite in self.game.all_sprites:
                    sprite.rect.x += PLAYER_SPEED * KNOCK_DISTANCE
                self.x_change -= PLAYER_SPEED * KNOCK_DISTANCE
            elif self.facing == "left":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= PLAYER_SPEED * KNOCK_DISTANCE
                self.x_change += PLAYER_SPEED * KNOCK_DISTANCE
            elif self.facing == "up":
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= PLAYER_SPEED * KNOCK_DISTANCE
                self.y_change += PLAYER_SPEED * KNOCK_DISTANCE
            elif self.facing == "down":
                for sprite in self.game.all_sprites:
                    sprite.rect.y += PLAYER_SPEED * KNOCK_DISTANCE
                self.y_change -= PLAYER_SPEED * KNOCK_DISTANCE

            pygame.time.wait(25)
            LIVES -= 1
            print(LIVES)

            if LIVES <= 0:
                self.kill()
                self.game.playing = False



    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()
        self.rect.x += self.x_change
        self.collide_trees("x")
        self.rect.y += self.y_change
        self.collide_trees("y")

        self.x_change = 0
        self.y_change = 0

    def collide_trees(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.trees, False)
            if hits:
                if self.x_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.trees, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
                    self.rect.y = hits[0].rect.bottom


    def animate(self):
        Player_animation_animate(self)


class Attack(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x, self.y = x, y
        self.width, self.height = TILESIZE, TILESIZE

        self.animation_loop = 0
        if self.animation_loop == 0:
            self.collidable = True
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        attack_animation(self)

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        if self.collidable:
            hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
            if hits:
                pass

    def animate(self):
        attack_animation_animate(self)