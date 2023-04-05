
class Table:

    table = [[''] * 8] * 9

    def __init__(self):
        pass

    def __str__(self):
        res = str()
        for row in self.table:
            res += str(row) + f'\n'
        return res

import random
import time

class Figure:

    figure = list()
    kind = (random.randint(1,100) * time.time_ns()) % 15

    def __inti__(self):
        pass