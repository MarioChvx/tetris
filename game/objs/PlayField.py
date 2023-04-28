
import numpy as np


class PlayField:
    '''
    Tetris has a 40 x 10 table where only 20 rows are visible for the player.
    Some times it could be 21 o 22.

    Atributes:
        matrix
        bottom
    '''

    def __init__(self, width=10, height=20):
        self.matrix = np.zeros((width, height)).astype(int)
        self.bottom = self.calculate_bottom()

    def calculate_bottom(self):
        pass

    def bottom_add_squqres(self, x: list, y: list):
        self.bottom['x'].extend(x)
        self.bottom['y'].extend(y)

    def remove_rows(self):
        pass

    def __str__(self):
        return ''.join([f'{row}\r\n' for row in self.matrix])
