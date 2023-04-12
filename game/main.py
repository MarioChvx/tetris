
import pygame
# import Table
import copy

SQUARE_SIDE = 40
SCREEN = {'h': 1000, 'w': 400}
GAME_AREA = {'h': 880, 'w': 400}
SURF = pygame.display.set_mode((SCREEN['w'], SCREEN['h']))
FPS = 60
COLORS = {
    'cyan':     (000, 255, 255),
    'yellow':   (255, 255, 000),
    'purple':   (128, 000, 128),
    'green':    (000, 128, 000),
    'red':      (255, 000, 000),
    'blue':     (000, 000, 255),
    'black':    (000, 000, 000),
    'orange':   (255, 165, 000),
    'white':    (255, 255, 255),
    'gray':     (128, 128, 128)
}

def draw_window(tetrimino, bottom_squares):
    SURF.fill(COLORS['black'])
    pygame.draw.rect(SURF, *tetrimino)
    draw_bootom(bottom_squares)
    pygame.display.flip()
    pygame.display.update()

def draw_bootom(bottom_squares):
    for square in bottom_squares:
        pygame.draw.rect(SURF, *square)


def tetri_movement(keys_pressed, tetrimino):
    if keys_pressed[pygame.K_a] and tetrimino.x - SQUARE_SIDE >= 0:
        tetri_xy[0] -= SQUARE_SIDE
    if keys_pressed[pygame.K_d] and tetrimino.x + SQUARE_SIDE <= GAME_AREA['w'] - SQUARE_SIDE:
        tetri_xy[0] += SQUARE_SIDE
    if keys_pressed[pygame.K_s] and tetrimino.y + SQUARE_SIDE <= GAME_AREA['h'] - SQUARE_SIDE:
        tetri_xy[1] += SQUARE_SIDE
    if keys_pressed[pygame.K_w] and tetrimino.y - SQUARE_SIDE >= 0:
        tetri_xy[1] -= SQUARE_SIDE
    
    if tetri_touchs_botom(tetrimino, bottom):
        bottomino = copy.deepcopy(tetrimino)
        bottom.append(bottomino)
        # tetrimino.x, tetrimino.y = [160, 0]
        tetri_xy = [160, 0]

    tetrimino.x, tetrimino.y = tetri_xy

def tetri_touchs_botom(tetriminio, bottom_squares):
    # tetriminio = tetriminio[0]
    if tetriminio.y == GAME_AREA['h'] - SQUARE_SIDE:
        return True
    for square in bottom_squares:
        if tetriminio.y - SQUARE_SIDE == square.y:
            return True


tetri_xy = [160, 0]
bottom = list()

def main():
    clock = pygame.time.Clock()
    pygame.display.set_caption('Tetris')
    tetrimino = (COLORS['cyan'], pygame.Rect(*tetri_xy, SQUARE_SIDE, SQUARE_SIDE))
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # print('exit event')
                run = False

        keys_pressed = pygame.key.get_pressed()
        tetri_movement(keys_pressed, tetrimino[1])
        draw_window(tetrimino, bottom)

    pygame.quit()

if __name__ == '__main__':
    main()