
class Cartesian:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y))


class Index:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y))
