
import pygame
from Tetrimino import Tetrimino

SQUARE_SIZE = 40
GAME_SURF = pygame.Surface(GAME_SIZE := (400, 800))
# returns a surface the size of the screen
DISPLAY_SURF = pygame.display.set_mode(DISPLAY_SIZE := (408, 900))
FPS = 10

def main():
    clock = pygame.time.Clock()
    piece = Tetrimino(SQUARE_SIZE)
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # print('exit event')
                run = False
        keys_pressed = pygame.key.get_pressed()
        tetri_movement(keys_pressed, piece)
        draw_window(piece)

    pygame.quit()

def draw_window(tetri: Tetrimino):
    GAME_SURF.fill(pygame.Color('black'))
    DISPLAY_SURF.fill(pygame.Color('gray'))
    tetri.draw(GAME_SURF)
    DISPLAY_SURF.blit(GAME_SURF, (4, 4))
    pygame.display.update()

def tetri_movement(keys_pressed, tetri: Tetrimino):

    if keys_pressed[pygame.K_a] and tetri.min_x - SQUARE_SIZE >= 0:
        tetri.move_left()

    if keys_pressed[pygame.K_d] and tetri.max_x + SQUARE_SIZE <= GAME_SIZE[0] - SQUARE_SIZE * tetri.width:
        tetri.move_right()

    if keys_pressed[pygame.K_s] and tetri.max_y + SQUARE_SIZE <= GAME_SIZE[1] - SQUARE_SIZE * tetri.height:
        tetri.move_down()

    if keys_pressed[pygame.K_w] and tetri.min_y - SQUARE_SIZE >= 0:
        tetri.move_up()

    if keys_pressed[pygame.K_r]:
        tetri.rotate()



if __name__ == '__main__':
    main()