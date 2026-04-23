import pygame
import sys
from settings import *


class GameManager:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(
            (ScreenSettings.WIDTH, ScreenSettings.HEIGHT)
        )
        pygame.display.set_caption(ScreenSettings.TITLE)
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(ColorSettings.SCREEN_BACKGROUND)
            pygame.display.flip()
            self.clock.tick(ScreenSettings.FPS)

        pygame.quit()


if __name__ == "__main__":
    game = GameManager()
    game.run()