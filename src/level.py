import pygame
from .settings import *
from .player import Player
from .enemy import Enemy


class Level:
    def __init__(self):
        # self.screen = screen
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()

        self.detector = None

        self.setup()

    def setup(self):
        self.player = Player((640, 360), self.all_sprites, self.display_surface)
        self.enemy = Enemy((600, 360), self.all_sprites, self.display_surface)
        self.enemy.player = self.player
        
    def run(self, dt):
        self.player.detector = self.detector

        self.display_surface.fill("black")
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)