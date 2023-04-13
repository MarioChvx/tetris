
import pygame
import sys
from Tetrimino import Tetrimino


GAME_SURF = pygame.Surface(GAME_SIZE := (400, 800))
SQUARE_SIZE = GAME_SIZE[0] // 10
# returns a surface the size of the screen
DISPLAY_SURF = pygame.display.set_mode(DISPLAY_SIZE := (408, 900))
FPS = 15


def main():
    clock = pygame.time.Clock()
    piece = Tetrimino(SQUARE_SIZE)
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                run = False
            tetri_controls(event, piece)

        draw_window(piece)

    pygame.quit()


def draw_window(tetri: Tetrimino):
    GAME_SURF.fill(pygame.Color('black'))
    DISPLAY_SURF.fill(pygame.Color('gray'))
    tetri.draw(GAME_SURF)
    DISPLAY_SURF.blit(GAME_SURF, (4, 4))
    pygame.display.update()


def tetri_controls(event, tetri):
    if event.type == pygame.KEYDOWN:
        if event.key in [pygame.K_LEFT, ord('a')] \
        and tetri.min_x - SQUARE_SIZE >= 0:
            tetri.move_left()
        if event.key in [pygame.K_RIGHT, ord('d')] \
        and tetri.max_x + SQUARE_SIZE <= GAME_SIZE[0]:
            tetri.move_right()
        if event.key in [pygame.K_DOWN, ord('s')] \
        and tetri.max_y + SQUARE_SIZE <= GAME_SIZE[1]:
            tetri.move_down()
        if event.key in [pygame.K_UP, ord('w')]:
            tetri.rotate()


if __name__ == '__main__':
    main()