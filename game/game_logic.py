from objs import PlayField
from objs import Tetrimino
import copy


"""
This is going to use PlayField and Tetrimino to control the game logic
"""


def print_plafield(pf: PlayField, te: Tetrimino):
    y, x = te.idx['y'], te.idx['x']
    a, b = te.matrix.shape
    tetri = copy.copy(te.matrix)
    print(tetri, tetri[1, :])
    before = True
    top, bottom = 0, 0
    for i in range(tetri.shape[0]):
        if 1 not in tetri[i, :] and before:
            top += 1
        elif 1 in tetri[i, :]:
            before = False
        elif 1 not in tetri[i, :] and not before:
            bottom += 1

    before = True
    left, right = 0, 0
    for i in range(tetri.shape[1]):
        if 1 not in tetri[:, i] and before:
            left += 1
        elif 1 in tetri[:, i]:
            before = False
        elif 1 not in tetri[:, i] and not before:
            right += 1
    print(tetri[top: a - bottom, left: b - right], top, bottom, left, right)
    tetri = tetri[top: a - bottom, left: b - right]
    # a, b = te.border['b'] - te.border['t'], te.border['r'] - te.border['l']
    printable = copy.copy(pf.matrix)
    # printable[y:y + a, x:x + b] += te.matrix
    printable[y + top:y + a - bottom, x + left:x + b - right] += tetri
    print(''.join([f'{row}\n' for row in printable]))


def tetrimino_actions(action: str, te: Tetrimino, pf: PlayField, times: int = 1):

    if action == 'l':  # and te.border['l'] - 1 <= 0:
        te.move_left()

    if action == 'r':  # and te.border['r'] + 1 <= pf.matrix.shape[1]:
        te.move_right()

    if action == 'u':  # and te.border['t'] - 1 >= 0:
        te.move_up()

    if action == 'd':  # and te.border['b'] + 1 <= pf.matrix.shape[0]:
        te.move_down()

    if action == 'rr':
        te.rotate()

    kick_in(te, pf)


def kick_in(te: Tetrimino, pf: PlayField):

    if te.border['t'] < 0:
        print('move down')
        te.move_down()

    if te.border['l'] < 0:
        print('move rigth')
        te.move_right()

    if te.border['r'] > pf.width - 1:
        print('move left')
        te.move_left()

    if te.border['b'] > pf.height - 1:  # or te_overlaps_pf(te, pf):
        print('move up')
        te.move_up()
        # append_bottom(te, pf)


def append_bottom(te: Tetrimino, pf: PlayField):
    pf.bottom_add_squares(te.coors)


def te_overlaps_pf(te: Tetrimino, pf: PlayField) -> bool:
    for coor in te.coors:
        if coor in pf.bottom:
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
