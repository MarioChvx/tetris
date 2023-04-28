from objs.PlayField import PlayField
from objs.NewTetrimino import Tetrimino
import pygame
import sys
from os import system


def print_plafield(pf: PlayField, te: Tetrimino):
    x, y = te.idx['x'], te.idx['y']
    a, b = te.matrix.shape
    printable = pf.matrix
    printable[y:y + b, x:x + a] += te.matrix
    print(''.join([f'{row}\n' for row in printable]))


def te_controls(event, te: Tetrimino, pf: PlayField):
    if event.type == pygame.KEYDOWN:
        if event.key in [pygame.K_LEFT, ord('a')] \
                and te.border['left'] - 1 >= 0:
            te.move_left()
        if event.key in [pygame.K_RIGHT, ord('d')] \
                and te.max_cart.x + 1 <= pf.matrix.shape[1]:
            te.move_right()
        if event.key in [pygame.K_DOWN, ord('s')] \
                and te.max_cart.y + 1 <= pf.matrix.shape[0]:
            te.move_down()
        if event.key in [pygame.K_UP, ord('w')]:
            te.rotate()
            # rotation_kick(te)


def main():
    play_field = PlayField(20, 10)
    new_tetri = Tetrimino()
    print_plafield(play_field, new_tetri)
    pass


FPS = 15


def main2():
    clock = pygame.time.Clock()
    run = True

    play_field = PlayField(20, 10)
    new_tetri = Tetrimino()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            te_controls(event, play_field, new_tetri)

        print_plafield(play_field, new_tetri)
        system('clear')

    pygame.quit()


if __name__ == '__main__':
    main()
