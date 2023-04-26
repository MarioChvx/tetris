from objs.PlayField import PlayField
from objs.NewTetrimino import Tetrimino


def print_plafield(pf: PlayField, te: Tetrimino):
    x, y = te.idx['x'], te.idx['y']
    a, b = te.matrix.shape
    printable = pf.matrix
    printable[y:y + b, x:x + a] += te.matrix
    print(''.join([f'{row}\n' for row in printable]))


def main():
    play_field = PlayField(20, 10)
    new_tetri = Tetrimino()
    print_plafield(play_field, new_tetri)
    pass


if __name__ == '__main__':
    main()
