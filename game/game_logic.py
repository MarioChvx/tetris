from objs import PlayField
from objs import Tetrimino


def print_plafield(pf: PlayField, te: Tetrimino):
    x, y = te.idx['x'], te.idx['y']
    a, b = te.matrix.shape
    printable = pf.matrix
    printable[y:y + b, x:x + a] += te.matrix
    print(''.join([f'{row}\n' for row in printable]))


def tetrimino_actions(action: str, times: int, te: Tetrimino, pf: PlayField):

    if action == 'left' and te.border['left'] - 1 >= 0:
        te.move_left()

    if action == 'right' and te.border['rigth'] + 1 <= pf.matrix.shape[1]:
        te.move_right()

    if action == 'down' and te.border['down'] + 1 <= pf.matrix.shape[0]:
        te.move_down()

    if action == 'rotate':
        te.rotate()
        # rotation_kick(te)


def append_bottom(te: Tetrimino, pf: PlayField):
    
    pass


def main():
    play_field = PlayField(20, 10)
    new_tetri = Tetrimino()
    print_plafield(play_field, new_tetri)


if __name__ == '__main__':
    main()
