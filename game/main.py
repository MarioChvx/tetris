
import pygame
import sys
from Tetrimino import Tetrimino
from Coordinates import Cartesian as Cart
from Bottom import Bottom

GAME_SURF = pygame.Surface(GAME_SIZE := (400, 800))
SQUARE_SIZE = GAME_SIZE[0] // 10
# returns a surface the size of the screen
DISPLAY_SURF = pygame.display.set_mode(DISPLAY_SIZE := (408, 900))
FPS = 15

PIECES = list()

def main():
    clock = pygame.time.Clock()
    run = True
    PIECES.append(Tetrimino(SQUARE_SIZE))
    bott = Bottom(SQUARE_SIZE)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            tetri_controls(event, PIECES[-1])

        draw_window(PIECES[-1], bott)

        if touch_floor(PIECES[-1]):
            reset_tetri(bott)

    pygame.quit()


def draw_window(tetri: Tetrimino, bottom: Bottom):
    GAME_SURF.fill(pygame.Color('black'))
    DISPLAY_SURF.fill(pygame.Color('gray'))
    tetri.draw(GAME_SURF)
    bottom.draw(GAME_SURF)
    DISPLAY_SURF.blit(GAME_SURF, (4, 4))
    pygame.display.update()


def tetri_controls(event, tetri):
    if event.type == pygame.KEYDOWN:
        if event.key in [pygame.K_LEFT, ord('a')] \
        and tetri.min_cart.x - SQUARE_SIZE >= 0:
            tetri.move_left()
        if event.key in [pygame.K_RIGHT, ord('d')] \
        and tetri.max_cart.x + SQUARE_SIZE <= GAME_SIZE[0]:
            tetri.move_right()
        if event.key in [pygame.K_DOWN, ord('s')] \
        and tetri.max_cart.y + SQUARE_SIZE <= GAME_SIZE[1]:
            tetri.move_down()
        if event.key in [pygame.K_UP, ord('w')]:
            tetri.rotate()
            rotation_kick(tetri)

def rotation_kick(tetri):
    limit_x = GAME_SIZE[0]
    limit_y = GAME_SIZE[1]
    if tetri.min_cart.x < 0:
        tetri.move_right(abs(tetri.min_cart.x // SQUARE_SIZE))
    if tetri.max_cart.x > limit_x:
        tetri.move_left((tetri.max_cart.x - limit_x) // SQUARE_SIZE)
    if tetri.max_cart.y > limit_y:
        tetri.move_up((tetri.max_cart.y - limit_y) // SQUARE_SIZE)

def touch_floor(tetri):
    return tetri.max_cart.y == GAME_SIZE[1]

def reset_tetri(bottom: Bottom):
    bottom.add_rects(PIECES[-1].rects)
    PIECES.pop()
    PIECES.append(Tetrimino(SQUARE_SIZE))

if __name__ == '__main__':
    main()