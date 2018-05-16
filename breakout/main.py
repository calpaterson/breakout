import pygame
import pygame.locals

display_surface = None

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super()

def main():
    global display_surface
    pygame.init()
    display_surface = pygame.display.set_mode((640, 480))

    pygame.display.set_caption("Breakout")

    going = True
    while going:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                going = False


if __name__ == "__main__":
    main()
