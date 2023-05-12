
import numpy as np
import itertools


class PlayField:
    '''
    Tetris has a 40 x 10 table where only 20 rows are visible for the player.
    Some times it could be 21 o 22.

    Atributes:
        matrix
        bottom  Set of coordinates
    '''

    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.matrix = np.zeros((width, height)).astype(int)
        self.bottom = self.calculate_bottom()

    def calculate_bottom(self):
        res = list()
        for i, j in itertools.product(list(map(range, self.matrix.shape))):
            if self.matrix[i][j]:
                res.append([i, j])
        return res

    def bottom_add_squqres(self, squares: set):
        self.bottom.update(squares)

    def remove_rows(self):
        pass

    def __str__(self):
        return ''.join([f'{row}\r\n' for row in self.matrix])
