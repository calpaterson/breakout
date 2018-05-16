import sys
from logging import getLogger, INFO, basicConfig

import pygame
import pygame.locals

logger = getLogger(__name__)

display_surface = None

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.gray = (192, 192, 192)
        self.width = 640/6
        self.image = pygame.Surface((self.width, 480/50)).convert()
        self.image.fill(self.gray)

        self.rect = self.image.get_rect()
        self.midtop_x = (480/5) * 4
        self.rect.midtop = (640/2, self.midtop_x)

    def update(self):
        mouse_position = pygame.mouse.get_pos()
        max_y = 640 - (0.5 * self.width)
        min_y = 0.5 * self.width
        midtop_y = max(min(mouse_position[0], max_y), min_y)
        self.rect.midtop = (midtop_y, self.midtop_x)

def main():
    global display_surface
    pygame.init()

    pygame.display.set_caption("Breakout")

    display_surface = pygame.display.set_mode((640, 480))

    background = pygame.Surface(display_surface.get_size()).convert()
    background.fill((0, 0, 0))

    paddle = Paddle()
    allsprites = pygame.sprite.RenderPlain((paddle,))

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                going = False
                sys.exit(1)

        allsprites.update()

        display_surface.blit(background, (0, 0))
        allsprites.draw(display_surface)
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    basicConfig(level=INFO)
    main()
