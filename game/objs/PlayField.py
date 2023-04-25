
import numpy as np


class PlayField:
    '''
    Tetris has a 40 x 10 table where only 20 rows are visible for the player.
    Some times it could be 21 o 22.
    '''

    def __init__(self, width=10, height=20):
        self.matrix = np.zeros((width, height))
        self.bottom = list()

    def calculate_bottom_coors(self):
        pass

    def add_rects(self, rects: list):
        for rect in rects:
            self.rects.append(rect)

    def remove_rows(self):
        pass

    def __str__(self):
        return str([str(row) + '\n' for row in self.matrix])
