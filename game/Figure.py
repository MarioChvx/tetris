import random
import time

O = [
    [1, 1],
    [1, 1]
]
S = [
    [0, 1, 1],
    [1, 1, 0]
]
Z = [
    [1, 1, 0],
    [1, 1, 1]
]
L = [
    [1, 0],
    [1, 0],
    [1, 1]
]
I = [
    [1],
    [1],
    [1],
    [1]
]
T = [
    [1, 1, 1],
    [0, 1, 0]
]

kinds = [O, S, L, I, T, Z]

class Figure:

    figure = kinds[(random.randint(1, 100) * time.time_ns()) % len(kinds)]
    shape = (len(figure), len(figure[0]))

    def __inti__(self):
        pass

    def __str__(self):
        res = str()
        for row in self.figure:
            res += str(row) + f'\n'
        return res

    def rotate_right(self):
        rotated = [[] * self.shape[1]]
        for row in self.figure:
            for n in row:
                pass
        pass
