
import numpy as np


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
        self.matrix = np.zeros((height, width)).astype(int)
        self.bottom = self.calculate_bottom()

    def calculate_bottom(self):
        res = list()
        for i in range(self.height):
            for j in range(self.width):
                if self.matrix[i][j]:
                    res.append([i, j])
        return res

    def bottom_add_squares(self, squares: list):
        self.bottom.extend(squares)
        for i, j in self.bottom:
            self.matrix[i][j] = 1

    def remove_rows(self):
        pass

    def __str__(self):
        return ''.join([f'{row}\r\n' for row in self.matrix])
