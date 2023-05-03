import random
import time
import numpy as np
import itertools


class Tetrimino:
    """ The shape that spawns at the top of the game

    Atributes:
        shape_type  An index that represents that represents the figure.
        matrix      Numpy array that has the representation of the figure.
        color       It depends on the shape_type.
        idx         The position of the top-left cornner.
        coor        Coordinates of each square from the figure.
        border      The max bottom and rigth coordinates.
    """

    s = [[1]]

    I = [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

    O = [[1, 1],
         [1, 1]]

    T = [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]]

    S = [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]]

    Z = [[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]]

    J = [[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]]

    L = [[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]]

    kinds = [I, O, T, S, Z, J, L]
    colors = [
        (000, 255, 255, 255),  # cyan
        (255, 255, 000, 255),  # yellow
        (128, 000, 128, 255),  # purple
        (000, 255, 000, 255),  # green
        (255, 000, 000, 255),  # red
        (000, 000, 255, 255),  # blue
        (255, 165, 000, 255),  # orange
        ]

    def __init__(self, shape_type: int = -1):
        if shape_type in range(8):
            self.shape_type = shape_type
        else:
            self.shape_type = (random.randint(1, 100) * time.time_ns()) \
                                % len(Tetrimino.kinds)
        self.matrix = np.array(Tetrimino.kinds[self.shape_type]).astype(int)
        self.color = Tetrimino.colors[self.shape_type]
        self.idx = {'x': 0, 'y': 0}
        self.coors = self.calculate_coors()
        self.border = self.calculate_border()

    def calculate_coors(self):
        res = set()
        x, y = self.idx['x'], self.idx['y']
        for i, j in itertools.product(list(map(range, self.matrix.shape))):
            if self.matrix[i][j] == 1:
                res.add([y + i, x + j])
        return res

    def calculate_border(self):
        x = [c[1] for c in self.coors]
        y = [c[1] for c in self.coors]
        return {
                'top':  min(x),
                'left': min(y),
                'bot':  max(x),
                'rigth': max(y)
                }

    def move_left(self, units=1):
        self.idx['x'] -= units
        for coor in self.coors:
            coor[0] -= units

    def move_right(self, units=1):
        self.idx['x'] += units
        for coor in self.coors:
            coor[0] += units

    def move_down(self, units=1):
        self.idx['y'] += units
        for coor in self.coors:
            coor[1] += units

    def move_up(self, units=1):
        self.idx['y'] -= units
        for coor in self.coors:
            coor[1] -= units

    def rotate(self, times=1):
        self.matrix = np.rot90(self.matrix, times)
        self.coors = self.calculate_coors()

    def __str__(self):
        return str([str(row) + '\n' for row in self.matrix])
