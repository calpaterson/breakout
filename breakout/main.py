import sys

import pygame
import pygame.locals

display_surface = None

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.gray = (192, 192, 192)
        self.image = pygame.Surface((100, 10))
        self.image.fill(self.gray)

        self.rect = self.image.get_rect()

def main():
    global display_surface
    pygame.init()
    display_surface = pygame.display.set_mode((640, 480))

    pygame.display.set_caption("Breakout")

    paddle = Paddle()
    allsprites = pygame.sprite.RenderPlain((paddle,))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                going = False
                sys.exit(1)

        allsprites.update()
        allsprites.draw(display_surface)
        pygame.display.flip()


if __name__ == "__main__":
    main()
