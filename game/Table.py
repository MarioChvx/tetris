import numpy as np 
class Table:

    '''
    Tetris has a 40 x 10 table where only 20 rows are visible for the player.
    Some times it could be 21 o 22. 
    '''

    def __init__(self, width, height, ):
        self.colors = [[''] * width] * height
        self.occupied = np.zeros((width, height))
        self.positions = np.zeros((width, height))

    def __str__(self):
        res = str()
        for row in self.table:
            res += str(row) + f'\n'
        return res

