from objs import PlayField
from objs import Tetrimino
import copy


"""
This is going to use PlayField and Tetrimino to control the game logic
"""


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

    kick_in(te, pf)


def kick_in(te: Tetrimino, pf: PlayField):

    if te.border['t'] < 0:
        te.move_down()

    if te.border['b'] > pf.height or te_overlaps_pf(te, pf):
        te.move_up()
        append_bottom(te, pf)

    if te.border['r'] > pf.width:
        te.move_left()

    if te.border['l'] < 0:
        te.move_rigth()


def append_bottom(te: Tetrimino, pf: PlayField):
    pf.bottom_add_squares(te.coors())


def te_overlaps_pf(te: Tetrimino, pf: PlayField) -> bool:
    for coor in te.coors:
        if coor in pf.coors:
            return False
    return True


def overlaps_in_next(te: Tetrimino, pf: PlayField) -> bool:
    temp = copy.copy(te)
    temp.move_down()
    return te_overlaps_pf(te, pf)


def main():
    play_field = PlayField(20, 10)
    new_tetri = Tetrimino()
    print_plafield(play_field, new_tetri)


if __name__ == '__main__':
    main()
