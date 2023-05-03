
import numpy as np 
import pygame
from objs.Coordinates import Index as Idx, Cartesian as Cart

class Bottom:

    '''
    Tetris has a 40 x 10 table where only 20 rows are visible for the player.
    Some times it could be 21 o 22. 
    '''

    def __init__(self, square_size, width = 10, height = 20):
        self.square_size = square_size
        self.matrix = np.zeros((width, height))
        self.size = Cart(width * square_size, height * square_size)
        self.rects = self.define_rects()

    def define_rects(self):
        rects = list()
        min_x, min_y = 0, 0
        x, y = min_x, min_y
        for row in self.matrix:
            for square in row:
                if square == 1:
                    rects.append(pygame.Rect(x, y, self.square_size, self.square_size))
                x += self.square_size
            x = min_x
            y += self.square_size
        return rects

    def draw(self, draw_surf):
        for rect in self.rects:
            pygame.draw.rect(
                surface = draw_surf,
                color = pygame.Color("gray30"),
                rect = rect,
                width = 3,
                border_radius = 5
            )

    def add_rects(self, rects: list):
        for rect in rects:
            self.rects.append(rect)

    def remove_rows(self):
        pass

    def __str__(self):
        return str([str(row) + f'\n' for row in self.matrix])

