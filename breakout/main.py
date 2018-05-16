import sys
from logging import getLogger, INFO, basicConfig
from enum import Enum

import pygame
import pygame.locals

logger = getLogger("breakout")

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


class Puck(pygame.sprite.Sprite):
    class LastContact(Enum):
        PADDLE = 1
        WALL = 2
        CEILING = 3

    def __init__(self, paddle):
        pygame.sprite.Sprite.__init__(self)
        self.white = (254, 254, 254)
        self.width = 480/50
        self.height = 480/50
        self.image = pygame.Surface((self.width, self.height)).convert()
        self.image.fill(self.white)

        self.rect = self.image.get_rect()
        self.rect.midbottom = paddle.rect.midtop

        self.paddle = paddle

        self.served = False
        self.x_direction = -1
        self.y_direction = -1
        self.last_contact = Puck.LastContact.PADDLE

    def update(self):
        on_ceiling = self.rect.top <= 0
        on_wall = any([
            self.rect.left <= 0,
            self.rect.right >= 640
        ])
        on_paddle = all([
            self.rect.colliderect(self.paddle.rect),
            self.last_contact != Puck.LastContact.PADDLE,
        ])
        on_floor = self.rect.top > 480

        if on_floor:
            logger.info("on_floor")
            self.served = False
            self.x_direction = -1
            self.y_direction = -1
            self.last_contact = Puck.LastContact.PADDLE
        elif on_ceiling:
            logger.info("on_ceiling")
            self.x_direction *= -1
            self.last_contact = Puck.LastContact.CEILING
        elif on_wall:
            logger.info("on_wall")
            self.y_direction *= -1
            self.last_contact = Puck.LastContact.WALL
        elif on_paddle:
            logger.info("on_paddle")
            self.x_direction *= -1
            self.last_contact = Puck.LastContact.PADDLE

        if not self.served:
            self.rect.midbottom = self.paddle.rect.midtop
        else:
            self.rect.move_ip(2 * self.y_direction, 3 * self.x_direction)


def main():
    global display_surface
    pygame.init()

    logger.info("driver = %s", pygame.display.get_driver())

    pygame.display.set_caption("Breakout")

    display_surface = pygame.display.set_mode((640, 480))

    background = pygame.Surface(display_surface.get_size()).convert()
    background.fill((0, 0, 0))

    paddle = Paddle()
    puck = Puck(paddle)
    allsprites = pygame.sprite.RenderUpdates((paddle, puck))

    clock = pygame.time.Clock()

    loop_index = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                going = False
                sys.exit(1)
            elif event.type == pygame.MOUSEBUTTONUP:
                logger.info("mouse click")
                puck.served = True

        allsprites.update()

        display_surface.blit(background, (0, 0))
        updated_rects = allsprites.draw(display_surface)
        pygame.display.update(updated_rects)

        clock.tick(60)

        if loop_index > (60 * 5):
            loop_index = 0
            logger.info("FPS = %d", clock.get_fps())
        else:
            loop_index += 1


if __name__ == "__main__":
    basicConfig(level=INFO)
    main()
