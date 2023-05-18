
import pygame
import sys
from objs.Tetrimino import Tetrimino
from objs.PlayField import PlayField
import game_logic as gl

FPS = 15
SCALE = 40
SQUARE_SIZE = SCALE
# Container of the game
GAME_SURF = pygame.Surface(GAME_SIZE := (SCALE*10, SCALE*20))
# General container
DISPLAY_SURF = pygame.display.set_mode(DISPLAY_SIZE := (612, 808))


def main():
    clock = pygame.time.Clock()
    run = True

    tetrimino = Tetrimino()
    tetrimino_rects = calculate_tetri_rects(tetrimino, SCALE)

    play_field = PlayField()

    print(f'{tetrimino.idx=}\n{tetrimino.coors=}\n{tetrimino.border=}')
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                tetri_controls(event, tetrimino, tetrimino_rects, play_field)
                tetrimino_rects = calculate_tetri_rects(tetrimino, SCALE)

        draw_window(
                tetrimino,
                tetrimino_rects
                )

    pygame.quit()


def draw_window(
        te: Tetrimino,
        te_rects: list
        ):
    DISPLAY_SURF.fill(pygame.Color('gray'))
    GAME_SURF.fill(pygame.Color('black'))
    draw_tetri(te, te_rects, GAME_SURF)

    DISPLAY_SURF.blit(GAME_SURF, (4, 4))
    pygame.display.update()


def calculate_tetri_rects(te: Tetrimino, scale: int) -> list:
    rects = list()
    for coor in te.coors:
        rects.append(
            pygame.Rect(
                coor[1] * scale, coor[0] * scale,
                scale, scale)
            )
    return rects


def move_rects(rects: list, direction: str, scale: int, times: int = 1):
    if direction == 'l':
        def move(rect, scale, times): rect.x -= scale * times
    elif direction == 'r':
        def move(rect, scale, times): rect.x += scale * times
    elif direction == 'u':
        def move(rect, scale, times): rect.y -= scale * times
    elif direction == 'd':
        def move(rect, scale, times): rect.y += scale * times

    for rect in rects:
        move(rect, scale, times)


def draw_tetri(te: Tetrimino, rects: list, surf: pygame.Surface):
    for rect in rects:
        pygame.draw.rect(
            surface=surf,
            color=te.color,
            rect=rect,
            width=3,
            border_radius=5
            )


def tetri_controls(e: pygame.event, te: Tetrimino, te_rects: list, pf: PlayField):
    if e.type == pygame.KEYDOWN:
        if e.key in [pygame.K_LEFT, ord('a')]:
            gl.tetrimino_actions('l', te, pf)
            #  move_rects(te_rects, 'l', SCALE)

        if e.key in [pygame.K_RIGHT, ord('d')]:
            gl.tetrimino_actions('r', te, pf)
            #  move_rects(te_rects, 'r', SCALE)

        if e.key in [pygame.K_DOWN, ord('s')]:
            gl.tetrimino_actions('d', te, pf)
            #  move_rects(te_rects, 'd', SCALE)

        if e.key in [pygame.K_UP, ord('w')]:
            gl.tetrimino_actions('u', te, pf)
            #  move_rects(te_rects, 'u', SCALE)

        print(f'{te.idx=}\n{te.coors=}\n{te.border=}')
        gl.print_plafield(pf, te)


if __name__ == '__main__':
    main()
