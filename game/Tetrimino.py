import random
import time
import pygame
import numpy as np

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

    def __init__(self, square_size):
        random_int = (random.randint(1, 100) * time.time_ns())
        self.square_size = square_size
        self.shape_index = random_int % len(Tetrimino.kinds)
        self.shape = Tetrimino.kinds[self.shape_index]
        self.color = Tetrimino.colors[self.shape_index]
        self.min_x = 0
        self.min_y = 0
        where = np.where(np.array(self.shape) == 1)
        self.width = max(where[1]) + 1
        self.height = max(where[0]) + 1
        self.max_x = self.square_size * self.width
        self.max_y = self.square_size * self.height
        self.rects = self.define_rects()

    def define_rects(self):
        rects = list()
        x, y = self.min_x, self.min_y
        for row in self.shape:
            for square in row:
                if square == 1:
                    rects.append(pygame.Rect(x, y, self.square_size, self.square_size))
                x += self.square_size
            x = self.min_x
            if 1 in row:
                y += self.square_size
        return rects

    def move_left(self, units = 1):
        total_move = units * self.square_size
        self.min_x -= total_move
        self.max_x -= total_move
        for square in self.rects:
            square.x -= total_move

    def move_right(self, units = 1):
        total_move = units * self.square_size
        self.min_x += total_move
        self.max_x += total_move
        for square in self.rects:
            square.x += total_move

    def move_down(self, units = 1):
        total_move = units * self.square_size
        self.min_y += total_move
        self.max_y += total_move
        for square in self.rects:
            square.y += total_move

    def move_up(self, units = 1):
        total_move = units * self.square_size
        self.min_y -= total_move
        self.max_y -= total_move
        for square in self.rects:
            square.y -= total_move

    def rotate(self, times = 1):


        self.shape = [[row[-i-1] for row in self.shape] for i in range(len(self.shape[0]))]
        self.height = len(self.shape)
        self.width = len(self.shape[0])
        self.max_x = self.square_size * self.width
        self.max_y = self.square_size * self.height
        self.rects = self.define_rects()

    def draw(self, display: pygame.display):
        for rect in self.rects:
            pygame.draw.rect(display, self.color, rect)

    def __str__(self):
        # res = str()
        # for row in self.shape:
        #     res += str(row) + '\n'
        return str(self.shape)
