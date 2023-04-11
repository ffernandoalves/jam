import pygame
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
        pygame.display.set_caption("Jam")
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = Level()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # if event.type == pygame.KEYDOWN:

            dt = self.clock.tick() / 1000

            self.level.run(dt)
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()