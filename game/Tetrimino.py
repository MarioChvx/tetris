import random
import time
import pygame

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
         [0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0]]

    T = [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]]

    kinds = [I, J, L, O, S, T, Z]
    colors = [
        (000, 255, 255, 255), # cyan
        (255, 255, 000, 255), # yellow
        (128, 000, 128, 255), # purple
        (000, 128, 000, 255), # green
        (255, 000, 000, 255), # red
        (000, 000, 255, 255), # blue
        (255, 165, 000, 255), # orange
        ]

    def __init__(self, square_size):
        random_index = (random.randint(1, 100) * time.time_ns()) % len(Tetrimino.kinds)
        self.shape = Tetrimino.kinds[random_index]
        self.color = Tetrimino.colors[random_index]

        self.shape = Tetrimino.s # Hardcode s to test game
        self.color = (255, 255, 255, 255)

        self.rects = list()
        self.square_size = square_size
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        x, y = 0, 0
        for row in self.shape:
            for square in row:
                if square == 1:
                    self.rects.append(pygame.Rect(x, y, square_size, square_size))
                x += square_size
            y += square_size

    def move_left(self, units = 1):
        # check if is in game area
        # update mins or maxs
        for square in self.rects:
            square.x -= units * self.square_size

    def move_right(self, units = 1):
        # check if is in game area
        for square in self.rects:
            square.x += units * self.square_size

    def move_down(self, units = 1):
        # check if is in game area
        for square in self.rects:
            square.y += units * self.square_size

    def draw(self, display: pygame.display):
        for rect in self.rects:
            pygame.draw.rect(display, self.color, rect)
