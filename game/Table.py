class Table:

    table = [[''] * 8] * 9

    def __init__(self):
        pass

    def __str__(self):
        res = str()
        for row in self.table:
            res += str(row) + f'\n'
        return res

