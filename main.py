import pygame, sys

from sounds import *
from player import *
from map_build import build_map
import maps
from sprites import *
from config import *


pygame.display.set_caption("4-rest Quest")


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('OutlinePixel7Solid.ttf', 32)
        self.terrainsheet = Spritesheet('terrain1.png')
        self.character_spritesheet = Spritesheet('character.png')
        self.enemy_spritesheet = Spritesheet('enemy.png')
        self.attack_spritesheet = Spritesheet('attack.png')
        self.intro_background = pygame.image.load("background.png")

    def createTilemap(self, tilemap):
        build_map(self, tilemap)

    def new(self, tilemap):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.trees = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.createTilemap(tilemap)

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill('black')
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)

        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def intro_screen(self, startresume):
        intro = True

        title = self.font.render("Main Menu", True, "white")
        title_rect = title.get_rect(x=280, y=100)

        play_button = Button(WIN_WIDTH/2-BTN_W/2, 200, BTN_W, BTN_H, 'black', 'gray', f"{startresume} Game", 32)
        # (self, x, y, width, height, fg, bg, content, fontsize)
        exit_button = Button(WIN_WIDTH/2-BTN_W/2, 400, BTN_W, BTN_H, 'black', 'gray', "Exit Game", 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            elif exit_button.is_pressed(mouse_pos, mouse_pressed):
                self.running = False
                pygame.quit()
                sys.exit()


            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


TILEMAP = maps.world_1.stage_1
game = Game()
game.intro_screen("Start")
game.new(TILEMAP)
while game.running:
    game.main()

pygame.quit()
sys.exit()