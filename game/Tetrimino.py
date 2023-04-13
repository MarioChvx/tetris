import random
import time
import pygame
import numpy as np
from Coordinates import Index as Idx, Cartesian as Cart

class Tetrimino:

    s = [[1]]

    O = [[1, 1],
         [1, 1]]

    S = [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]]

    Z = [[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]]

    L = [[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]]

    J = [[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]]

    I = [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

    T = [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]]

    # O = [[1, 1],
    #      [1, 1]]

    # S = [[0, 1, 1],
    #      [1, 1, 0]]

    # Z = [[1, 1, 0],
    #      [0, 1, 1]]

    # L = [[0, 0, 1],
    #      [1, 1, 1]]

    # J = [[1, 0, 0],
    #      [1, 1, 1]]

    # I = [[1, 1, 1, 1]]

    # T = [[0, 1, 0],
    #      [1, 1, 1]]

    kinds = [I, O, T, S, Z, J, L]
    colors = [
        (000, 255, 255, 255), # cyan
        (255, 255, 000, 255), # yellow
        (128, 000, 128, 255), # purple
        (000, 255, 000, 255), # green
        (255, 000, 000, 255), # red
        (000, 000, 255, 255), # blue
        (255, 165, 000, 255), # orange
        ]

    def __init__(self, square_size, play_field):
        self.square_size = square_size
        self.shape_type = (random.randint(1, 100) * time.time_ns()) % len(Tetrimino.kinds)
        self.matrix = np.array(Tetrimino.kinds[self.shape_type])
        self.color = Tetrimino.colors[self.shape_type]
        self.min_idx = Idx(0, 0)
        self.min_cart = Cart(0, 0)
        self.width = np.any(np.array(self.matrix) == 1, axis=0).sum()
        self.height = np.any(np.array(self.matrix) == 1, axis=1).sum()
        self.max_idx = Idx(self.height - 1, self.width - 1)
        self.rects = self.define_rects()

    def define_rects(self):
        rects = list()
        x, y = self.min_cart.x, self.min_cart.y
        for row in self.matrix:
            for square in row:
                if square == 1:
                    rects.append(pygame.Rect(x, y, self.square_size, self.square_size))
                x += self.square_size
            x = self.min_cart.x
            if 1 in row:
                y += self.square_size
        return rects

    def move_left(self, units = 1):
        self.min_idx.x -= units
        self.max_idx.x -= units
        total_move = units * self.square_size
        self.min_cart.x -= total_move
        self.max_cart.x -= total_move
        for square in self.rects:
            square.x -= total_move

    def move_right(self, units = 1):
        self.min_idx.x += units
        self.max_idx.x += units
        total_move = units * self.square_size
        self.min_cart.x += total_move
        self.max_cart.x += total_move
        for square in self.rects:
            square.x += total_move

    def move_down(self, units = 1):
        self.min_idx.y += units
        self.max_idx.y += units
        total_move = units * self.square_size
        self.min_cart.y += total_move
        self.max_cart.y += total_move
        for square in self.rects:
            square.y += total_move

    def move_up(self, units = 1):
        self.min_idx.y -= units
        self.min_idx.y -= units
        total_move = units * self.square_size
        self.min_cart.y -= total_move
        self.max_cart.y -= total_move
        for square in self.rects:
            square.y -= total_move

    def rotate(self, times = 1):
        self.matrix = np.rot90(self.matrix, times)
        self.width = np.any(np.array(self.matrix) == 1, axis=0).sum()
        self.height = np.any(np.array(self.matrix) == 1, axis=1).sum()
        print(np.where(np.all(self.matrix == 0, axis = 0)))
        self.max_x = self.min_x + self.square_size * self.width
        self.max_y = self.min_y + self.square_size * self.height
        self.rects = self.define_rects()

    def draw(self, draw_surf: pygame.Surface):
        for rect in self.rects:
            pygame.draw.rect(
                surface = draw_surf,
                color = self.color,
                rect = rect,
                width = 3,
                border_radius = 5
            )

    def __str__(self):
        return str([str(row) + f'\n' for row in self.matrix])
