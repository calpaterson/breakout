import sys
from logging import getLogger, INFO, basicConfig
from enum import Enum
import random

import pygame
import pygame.locals

logger = getLogger("breakout")

WIDTH = 1024
HEIGHT = 800

display_surface = None

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.gray = (192, 192, 192)
        self.width = WIDTH/6
        self.image = pygame.Surface((self.width, HEIGHT/50)).convert()
        self.image.fill(self.gray)

        self.rect = self.image.get_rect()
        self.midtop_x = (HEIGHT/5) * 4
        self.rect.midtop = (WIDTH/2, self.midtop_x)

    def update(self):
        mouse_position = pygame.mouse.get_pos()
        max_y = WIDTH - (0.5 * self.width)
        min_y = 0.5 * self.width
        midtop_y = max(min(mouse_position[0], max_y), min_y)
        self.rect.midtop = (midtop_y, self.midtop_x)


class Puck(pygame.sprite.Sprite):
    class LastContact(Enum):
        PADDLE = 1
        WALL = 2
        CEILING = 3
        BLOCK = 4

    def __init__(self, paddle, blocks):
        pygame.sprite.Sprite.__init__(self)
        self.white = (254, 254, 254)
        self.width = HEIGHT/50
        self.height = HEIGHT/50
        self.image = pygame.Surface((self.width, self.height)).convert()
        self.image.fill(self.white)

        self.rect = self.image.get_rect()
        self.rect.midbottom = paddle.rect.midtop

        self.paddle = paddle
        self.blocks = blocks

        self.served = False
        self.x_direction = -1
        self.y_direction = -1
        self.last_contact = Puck.LastContact.PADDLE

    def update(self):
        on_ceiling = self.rect.top <= 0
        on_wall = any([
            self.rect.left <= 0,
            self.rect.right >= WIDTH
        ])
        on_paddle = all([
            self.rect.colliderect(self.paddle.rect),
            self.last_contact != Puck.LastContact.PADDLE,
        ])
        on_floor = self.rect.top > HEIGHT
        block_sprites = self.blocks.sprites()
        on_block = self.rect.collidelist(block_sprites)

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
        elif on_block != -1:
            logger.info(on_block)
            block_sprites[on_block].kill()
            self.last_contact = Puck.LastContact.BLOCK

        if not self.served:
            self.rect.midbottom = self.paddle.rect.midtop
        else:
            self.rect.move_ip(2 * self.y_direction, 3 * self.x_direction)


class Block(pygame.sprite.Sprite):
    class Level(Enum):
        EASIEST = 0
        EASY = 1
        HARD = 3
        HARDEST = 4


    level_colours = {
        Level.EASIEST: (230, 0, 230),
        Level.EASY: (230, 0, 0),
        Level.HARD: (0, 230, 0),
        Level.HARDEST: (0, 230, 230),
    }

    def __init__(self, level=Level.EASIEST):
        pygame.sprite.Sprite.__init__(self)

        self.level = level
        self.colour = Block.level_colours[level]
        self.width = WIDTH/15
        self.height = HEIGHT/25
        self.image = pygame.Surface((self.width, self.height)).convert()
        self.image.fill(self.colour)

        self.rect = self.image.get_rect()


def generate_blocks(n=13):
    rng = random.Random(0)
    blocks = pygame.sprite.Group(
        Block(level=rng.choice(list(Block.Level))) for _ in range(n))

    block_height = blocks.sprites()[0].rect.height
    block_width = blocks.sprites()[0].rect.width

    topleft = (block_width, block_height)
    for index, block in enumerate(blocks, start=1):
        block.rect.topleft = topleft
        logger.info(topleft)

        if index % 13 == 0:
            topleft = (block_width, ((index // 13) + 1) * block_height)
        else:
            topleft = block.rect.topright
    return blocks



def main():
    global display_surface
    pygame.init()

    logger.info("driver = %s", pygame.display.get_driver())

    pygame.display.set_caption("Breakout")

    display_surface = pygame.display.set_mode((WIDTH, HEIGHT))

    background = pygame.Surface(display_surface.get_size()).convert()
    background.fill((0, 0, 0))

    paddle = Paddle()
    blocks = generate_blocks(n=13*5)
    puck = Puck(paddle, blocks)
    allsprites = pygame.sprite.RenderUpdates()
    allsprites.add(paddle)
    allsprites.add(puck)
    for block in blocks:
        allsprites.add(block)

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
