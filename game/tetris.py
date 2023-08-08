import pygame
import random
from copy import copy, deepcopy
from Block import blocks, BLACK, GRAY, WHITE, RED
from Grid import Grid

# Initialize Pygame
pygame.init()

# Define block size
BLOCK_SIZE = 40

# Set up the game window
WIDTH, HEIGHT = 400, 800
WIN = pygame.display.set_mode((WIDTH + 200, HEIGHT))
GAME = pygame.Surface((400, 800))
STATS = pygame.Surface((200, 800))
pygame.display.set_caption("Tetris")

BLOCKS = blocks

# Calculate the number of blocks that fit the screen
GRID_WIDTH = WIDTH // BLOCK_SIZE
GRID_HEIGHT = HEIGHT // BLOCK_SIZE

# Timer for fall
FALL_TIMER = pygame.USEREVENT + 1
IA_TIMER = pygame.USEREVENT + 2

# font
PIXEL_FONT = pygame.font.Font()


def draw_grid_lines():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(GAME, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(GAME, GRAY, (0, y), (WIDTH, y))


def draw_square_block(x, y, color):
    pygame.draw.rect(GAME, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def draw_square_grid(x, y, color):
    pygame.draw.rect(GAME, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def draw_square_prediction(x, y, color):
    pygame.draw.rect(
        GAME,
        color,
        (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
        BLOCK_SIZE // 12
    )


def draw_block_n_prediction(block, x, y, grid):
    p = prediction(block.shape, x, y, grid)
    n = len(block.shape)
    for row in range(n):
        for col in range(n):
            if block.shape[row][col]:
                draw_square_prediction(x + col, p + row, block.color)
                draw_square_block(x + col, y + row, block.color)
                

def draw_block_n_prediction2(block, x, y, grid):
    p = hard_drop(block.short_shape, x, grid)
    for row in range(len(block.short_shape)):
        for col in range(len(block.short_shape[0])):
            if block.short_shape[row][col]:
                draw_square_prediction(x + col, p + row, block.color)
                draw_square_block(x + col, y + row, block.color)


def draw_grid(grid):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid.shape[row][col]:
                draw_square_block(col, row, grid.colors[row][col])


def draw_stats_lines(surf):
    pygame.draw.line(STATS, WHITE, (0, 0), (0, HEIGHT))
    pygame.draw.line(STATS, WHITE, (0, 200), (200, 200))


def draw_next_block(surf, block):
    xp = (200 - 40 * len(block.short_shape[0])) // 2
    yp = (200 - 40 * len(block.short_shape)) // 2
    for row in range(len(block.short_shape)):
        for col in range(len(block.short_shape[0])):
            if block.short_shape[row][col]:
                pygame.draw.rect(STATS, block.color, (col * BLOCK_SIZE + xp, row * BLOCK_SIZE + yp, BLOCK_SIZE, BLOCK_SIZE))


def draw_scores(surf, score, gravity, temp):
    font = pygame.font.Font(None, 36)
    punctuation = font.render(f'BLOCKS: {score}', True, WHITE)
    surf.blit(punctuation, (10, 210))
    punctuation = font.render(f'SPEED: {(1 / gravity) * 1000} B/s', True, WHITE)
    surf.blit(punctuation, (10, 260))
    punctuation = font.render(f'height: {temp[0]}', True, WHITE)
    surf.blit(punctuation, (10, 310))
    punctuation = font.render(f'fillnes: {temp[1]}', True, WHITE)
    surf.blit(punctuation, (10, 360))
    punctuation = font.render(f'holes: {temp[2]}', True, WHITE)
    surf.blit(punctuation, (10, 410))
    punctuation = font.render(f'full rows: {temp[3]}', True, WHITE)
    surf.blit(punctuation, (10, 460))


def draw_mode(surf, mode):
    font = pygame.font.Font(None, 36)
    punctuation = font.render(f'mode: {mode}', True, WHITE)
    surf.blit(punctuation, (10, 740))


def draw_game_over():
    font = pygame.font.Font(None, 64)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.blit(text, text_rect)


def draw_curr_game(surf, game_index):
    font = pygame.font.Font(None, 36)
    punctuation = font.render(f'game: {game_index}', True, WHITE)
    surf.blit(punctuation, (10, 700))


def create_block():
    return random.choice(BLOCKS)


def fill_blocks(blocks):
    while len(blocks) < 4:
        new_block = create_block()
        if new_block not in blocks:
            blocks.append(new_block)


def create_blocks():
    blocks = list()
    fill_blocks(blocks)
    return blocks


def check_collision(block, x, y, grid):
    for row in range(len(block)):
        for col in range(len(block[row])):
            if block[row][col] and (x + col < 0 or x + col >= GRID_WIDTH or
                                    y + row >= GRID_HEIGHT or grid[y + row][x + col]):
                return True
    return False


def keep_in(block, x, y, grid):
    max_x, min_x = 0, 0
    for row in range(len(block)):
        for col in range(len(block[row])):
            if block[row][col]:
                max_x = max_x if max_x > col else col
                min_x = min_x if min_x < col else col
    if min_x + x < 0:
        x = 0
    elif max_x + x > GRID_WIDTH - 1:
        x = GRID_WIDTH - len(block[0])

    return x


def rotate_matrix(matrix):
    return list(zip(*reversed(matrix)))


def calculate_holes(grid):
    grid = rotate_matrix(grid)
    holes = 0
    for col in grid:
        col = list(reversed(col))
        after = -1
        for n in range(len(col)):
            if col[n] == 1 and after == -1:
                after = n
            elif col[n] == 0 and after != -1:
                holes += 1
    return holes


def mean_height(grid):
    grid = rotate_matrix(grid)
    res = list()
    for col in grid:
        col = list(reversed(col))
        for i, n in enumerate(col):
            if n == 1:
                res.append(i)
    
    return sum(res) / len(res) if len(res) > 0 else 0


def calculate_scores(grid):
    max_height = 0
    fillness = 0
    for i, row in enumerate(grid):
        # max_height = len(grid) - i if 1 in grid[i] and not max_height else 0
        if 1 in grid[i]:
            max_height += 1
        for j in range(len(grid[0])):
            if grid[i][j]:
                fillness += 1
    return (max_height,
            fillness / (max_height * len(grid[0])) if max_height > 0 else 0,
            calculate_holes(grid),
            len(check_full_rows(grid)),
            mean_height(grid))


def merge_block(block, x, y, grid):
    n = len(block.shape)
    for row in range(n):
        for col in range(n):
            if block.shape[row][col]:
                grid.shape[y + row - 1][x + col] = 1
                grid.colors[y + row - 1][x + col] = block.color


def remove_row(grid, row):
    del grid.shape[row]
    del grid.colors[row]
    grid.shape.insert(0, [0] * GRID_WIDTH)
    grid.colors.insert(0, [None] * GRID_WIDTH)


def check_full_rows(grid):
    full_rows = list()
    for i in range(len(grid)):
        if all(grid[i]):
            full_rows.append(i)
    return full_rows


def prediction(block, x, y, grid):
    block_bottom = list()
    for col in range(len(block[0])):
        block_bottom.append(-1)
        for row in range(len(block)):
            if row > block_bottom[-1] and block[row][col]:
                block_bottom[-1] = row

    # checar si hay columna de 0 a la izquierda
    after = True
    for i in range(len(block_bottom)):
        if block_bottom[i] == -1:
            x = x + 1 if after else x
        else:
            after = False
    block_bottom = [i for i in block_bottom if i != -1]

    grid_top = list()
    end = x + len(block_bottom) if x + len(block_bottom) < 10 else 10
    for col in range(x, end):
        grid_top.append(len(grid))
        for row in range(len(grid)):
            if row < grid_top[col - x] and grid[row][col]:
                grid_top[col - x] = row

    return min([grid_top[i] - block_bottom[i] - 1 for i in range(len(grid_top))])


def hard_drop(block, x, grid):
    # el mas alto de cada columna
    block_bottom = list()
    for col in range(len(block[0])):
        block_bottom.append(-1)
        for row in range(len(block)):
            if row > block_bottom[-1] and block[row][col]:
                block_bottom[-1] = row

    grid_top = list()
    end = x + len(block_bottom) if x + len(block_bottom) < 10 else 10
    for col in range(x, end):
        grid_top.append(len(grid))
        for row in range(len(grid)):
            if row < grid_top[col - x] and grid[row][col]:
                grid_top[col - x] = row

    return min([grid_top[i] - block_bottom[i] - 1 for i in range(len(grid_top))])


def new_matrix(i, j, fill=0):
    res = list()
    for row in range(i):
        res.append([fill] * j)
    return res


def print_grid(grid, limit = 20):
    n = len(grid)
    for row in grid[n - limit: n]:
        print(row)


def check_movement(event, x, y, blocks, grid):
    if event.key in [pygame.K_LEFT, ord('a'), ord('A')] and not check_collision(blocks[0].shape, x - 1, y, grid):
        x -= 1
    elif event.key in [pygame.K_RIGHT, ord('d'), ord('D')] and not check_collision(blocks[0].shape, x + 1, y, grid):
        x += 1
    elif event.key in [pygame.K_DOWN, ord('s'), ord('S')] and not check_collision(blocks[0].shape, x, y + 1, grid):
        y += 1
    elif event.key in [pygame.K_UP, ord('w'), ord('W')]:
        blocks[0].shape = list(zip(*reversed(blocks[0].shape)))
        blocks[0].short_shape = list(zip(*reversed(blocks[0].short_shape)))
        x = keep_in(blocks[0].shape, x, y, grid)
    elif event.key in [pygame.K_SPACE]:
        p = prediction(blocks[0].shape, x, y, grid)
        y = p + 1
    elif event.key in [ord('h'), ord('H')]:
        blocks[0], blocks[1] = blocks[1], blocks[0]

    return x, y


def check_movement2(event, game_index, n):
    if event.key in [pygame.K_LEFT, ord('a'), ord('A')]:
        game_index = n if game_index == 0 else game_index - 1
    elif event.key in [pygame.K_RIGHT, ord('d'), ord('D')]:
        game_index = 0 if game_index == n else game_index + 1
    return game_index


def check_mode(event, mode):
    if event.key == pygame.K_F1 and mode != 1:
        tetris(1)
    elif event.key == pygame.K_F2 and mode != 2:
        tetris(2)
    elif event.key == pygame.K_F3 and mode != 3:
        tetris(3)
    else:
        pass


def merge_block2(block, x, y, grid):
    block_width = len(block.short_shape[0])
    block_height = len(block.short_shape)
    for row in range(block_height):
        for col in range(block_width):
            if block.short_shape[row][col]:
                grid.shape[y + row][x + col] = 1
                grid.colors[y + row][x + col] = block.color


def merge_block3(block, x, y, grid):
    block_width = len(block.short_shape[0])
    block_height = len(block.short_shape)
    for row in range(block_height):
        for col in range(block_width):
            if block.short_shape[row][col]:
                grid.shape[y + row - 1][x + col] = 1
                grid.colors[y + row - 1][x + col] = block.color



def shape_merge(block, x, y, grid) -> list:
    result = grid.copy()
    block_width = len(block[0])
    block_height = len(block)
    for row in range(block_height):
        for col in range(block_width):
            if block[row][col]:
                grid[y + row][x + col] += 1
    return result


def gen_all_posibilites(a, block, grid) -> list:
    grid_width = len(grid[0])
    block_m = block.short_shape
    posibilites = list()
    for t in range(block.turns):
        shape_width = len(block_m[0])
        for x in range(grid_width - shape_width + 1):
            y = hard_drop(block_m, x, grid)
            n_grid = deepcopy(grid)
            posibilites.append({
                'a': a,
                'turns': t,
                'moves': x,
                'y': y,
                'block': block_m,
                'shape': shape_merge(block_m, x, y, n_grid)
            })
            # print_grid(posibilites[-1]['shape'])
            # fail()
            n_grid = None
        block_m = rotate_matrix(block_m)
    return posibilites


def score_possibility(possibility: dict):
    t = possibility.copy()
    t['scores'] = calculate_scores(t['shape'])
    # t.pop('shape')
    return t


def eval_possibility(possibility: dict, weights: list):
    t = possibility.copy()
    t['eval'] = sum([t['scores'][i] + weights[i] for i in range(4)])
    # t.pop('scores')
    return t


# (max_height, fillnes, holes, full_rows, mean_height)
def manual_selection(posibilites: list()) -> list:
    # full_rows
    posibilites = sorted(posibilites, key=lambda p: p['scores'][3], reverse=True)[:(len(posibilites) // 2)]
    # mean_height
    posibilites = sorted(posibilites, key=lambda p: p['scores'][4], reverse=True)[:(len(posibilites) // 2)]
    # holes
    posibilites = sorted(posibilites, key=lambda p: p['scores'][2])[:(len(posibilites) // 2)]
    # fillnes
    posibilites = sorted(posibilites, key=lambda p: p['scores'][1], reverse=True)[:(len(posibilites) // 2)]
    return min(posibilites, key=lambda p: p['scores'][2])


def gen_vector(n):
    return [random.uniform(-10, 10) for _ in range(n)]


def merge_vectors(vectors: list):
    n = len(vectors)
    m = len(vectors[0])
    res = [0] * m
    for v in vectors:
        for w in range(m):
            res[w] = v[w]
    return [r / n for r in res]


def noise_vector(vector: list, strength: float):
    res = list()
    for w in vector:
        noise = random.uniform(-strength, strength)
        res.append(w + noise)
    return res


def move_to_key(move: dict) -> list:
    keys = list()
    if move['a'] == 1:
        keys.append('h')
    for _ in range(move['turns']):
        keys.append('r')
    for _ in range(move['moves']):
        keys.append('x')
    keys.append('y')
    return keys

def main(mode = 0):

    paused = False
    g = 1000
    pygame.time.set_timer(FALL_TIMER, g)
    pygame.time.set_timer(IA_TIMER, ia_delay := 100)
    clock = pygame.time.Clock()
    score = 0

    if mode in [0, 1]:
        mode1()
    elif mode == 2:
        mode2()
    elif mode == 3:
        mode2()

def mode1(mode):
    queue_blocks = create_blocks()
    curr_block = queue_blocks[0]
    grid = Grid(new_matrix(GRID_HEIGHT, GRID_WIDTH), new_matrix(GRID_HEIGHT, GRID_WIDTH, None))
    x, y = GRID_WIDTH // 2 - len(curr_block.shape) // 2, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

                # if event.key == pygame.K_ESCAPE:
                    # paused = not paused
            if event.type == pygame.KEYDOWN:
                x, y = check_movement(event, x, y, queue_blocks, grid.shape)
                curr_block = queue_blocks[0]

            if event.type == FALL_TIMER:
                y += 1
                pygame.time.set_timer(FALL_TIMER, g)
            
        if not paused:
            if check_collision(curr_block.shape, x, y, grid.shape):
                score += 1
                if score % 10 == 0:
                    # g = int(g * 0.9)
                    g -= 100
                merge_block(curr_block, x, y, grid)
                queue_blocks.pop(0)
                fill_blocks(queue_blocks)
                full_rows = check_full_rows(grid.shape)
                if full_rows:
                    for row in full_rows:
                        remove_row(grid, row)
                score += len(full_rows)
                curr_block = queue_blocks[0]
                x, y = GRID_WIDTH // 2 - len(curr_block.shape) // 2, 0
                if check_collision(curr_block.shape, x, y, grid.shape):
                    draw_game_over()
                    pygame.display.update()
                    return

            # Draw game
            WIN.fill(BLACK)

            STATS.fill(BLACK)
            draw_stats_lines(STATS)
            draw_mode(STATS, mode)
            draw_next_block(STATS, queue_blocks[1])
            draw_scores(STATS, score, g, calculate_scores(grid.shape))
            WIN.blit(STATS, (400, 0))

            GAME.fill(BLACK)
            draw_grid_lines()
            draw_grid(grid)
            draw_block_n_prediction(curr_block, x, y, grid.shape)
            WIN.blit(GAME, (0, 0))

            pygame.display.update()
            clock.tick(60)

def mode2():
    quantity_games = 100
    gen = 0
    queues_blocks = [create_blocks() for _ in range(quantity_games)]
    vectors = [noise_vector([-15, 5, -5, 15, -10], 1) for _ in range(quantity_games)]
    curr_blocks = [queues_blocks[i][0] for i in range(quantity_games)]
    grids = [Grid(new_matrix(GRID_HEIGHT, GRID_WIDTH), new_matrix(GRID_HEIGHT, GRID_WIDTH, None)) for _ in range(quantity_games)]
    X_arr, Y_arr = [0] * quantity_games, [0] * quantity_games
    curr_game = 0
    generation = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                check_mode(event, mode)
                if event.key == pygame.K_ESCAPE:
                    # paused = not paused
                    ...
                elif mode == 2:
                    curr_game = check_movement2(event, curr_game, len(grids) - 1)
                    grid = grids[curr_game]
                    x, y = X_arr[curr_game], Y_arr[curr_game]

            if event.type == FALL_TIMER:
                    Y_arr = [y + 1 for y in Y_arr]
                    pygame.time.set_timer(FALL_TIMER, g)
            
        if not paused:
            if len(grids) > quantity_games * .2:
                for i, grid in enumerate(grids):
                    posibilites = list()
                    posibilites.extend(gen_all_posibilites(0, queues_blocks[i][0], grids[i].shape))
                    posibilites.extend(gen_all_posibilites(1, queues_blocks[i][1], grids[i].shape))
                    posibilites = list(map(score_possibility, posibilites))
                    posibilites = manual_selection(posibilites)
                    posibilites = [eval_possibility(posibilites[j], vectors[i]) for j in range(len(posibilites))] 
                    best_move = max(posibilites, key=lambda p: p['eval'])
                    X_arr[i] = best_move['moves']
                    for _ in range(best_move['turns']):
                        queues_blocks[i][best_move['a']].short_shape = rotate_matrix(queues_blocks[i][best_move['a']].short_shape)
                    merge_block2(queues_blocks[i][best_move['a']], X_arr[i], best_move['y'], grids[i])
                    queues_blocks[i].pop(best_move['a'])
                    fill_blocks(queues_blocks[i])
                    full_rows = check_full_rows(grids[i].shape)
                    if full_rows:
                        for row in full_rows:
                            remove_row(grids[i], row)
                    score += len(full_rows)
                    curr_blocks[i] = queues_blocks[i][0]
                    X_arr[i], Y_arr[i] = 0, 0
                    if check_collision(curr_blocks[i].shape, X_arr[i], Y_arr[i], grids[i].shape):
                        grids.pop(i)
                        queues_blocks.pop(i)
                        curr_blocks.pop(i)
                        X_arr.pop(i)
                        Y_arr.pop(i)
                        vectors.pop(i)
                        pass
                score += 1
            elif generation < 100:
                generation += 1
                # merge vectors
                # print_grid(vectors)
                father_vector = merge_vectors(vectors)
                # create sons of vectors
                vectors = [noise_vector(father_vector, .1) for _ in range(quantity_games)]
                print(score)
                print(f'{generation} -> {father_vector}')
                # print(quantity_games)
                # print(len(vectors))
                # for i, v in enumerate(vectors):
                #     print(i, v, sep=' -> ')
                # restart games with new vectors
                queues_blocks = [create_blocks() for _ in range(quantity_games)]
                curr_blocks = [queues_blocks[i][0] for i in range(quantity_games)]
                vectors = [gen_vector(5) for _ in range(quantity_games)]
                grids = [Grid(new_matrix(GRID_HEIGHT, GRID_WIDTH), new_matrix(GRID_HEIGHT, GRID_WIDTH, None)) for _ in range(quantity_games)]
                X_arr, Y_arr = [0] * quantity_games, [0] * quantity_games
                curr_game = 0
                score = 0

            # Draw game
            WIN.fill(BLACK)

            STATS.fill(BLACK)
            draw_stats_lines(STATS)
            draw_mode(STATS, mode)
            if mode in [1, 3]:
                draw_next_block(STATS, queue_blocks[1])
                draw_scores(STATS, score, g, calculate_scores(grid.shape))
            elif mode == 2:
                draw_next_block(STATS, queues_blocks[curr_game][1])
                draw_scores(STATS, score, g, calculate_scores(grids[curr_game].shape))
                draw_curr_game(STATS, curr_game)
            WIN.blit(STATS, (400, 0))

            GAME.fill(BLACK)
            draw_grid_lines()
            draw_grid(grids[curr_game])
            draw_block_n_prediction2(
                queues_blocks[curr_game][0],
                X_arr[curr_game],
                Y_arr[curr_game],
                grids[curr_game].shape)
            WIN.blit(GAME, (0, 0))

            pygame.display.update()
            clock.tick(60)

def mode3(mode):
    queue_blocks = create_blocks()
    curr_block = queue_blocks[0]
    grid = Grid(new_matrix(GRID_HEIGHT, GRID_WIDTH), new_matrix(GRID_HEIGHT, GRID_WIDTH, None))
    vector = [0.30597562095730596, 0.3289219430509858, 0.1927463043567247, -0.33222141617137524, 0.331751450080265]
    x, y = 0, 0
    calculated = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_ESCAPE:
                    # paused = not paused
                    # ...
                    # check_movement
                curr_block = queue_blocks[0]

            if event.type == FALL_TIMER:
                y += 1
                pygame.time.set_timer(FALL_TIMER, g)
            
            if event.type == IA_TIMER:
                m = auto_moves.pop(0)
                if m == 'h':
                    print('switch')
                    queue_blocks[0], queue_blocks[1] = queue_blocks[1], queue_blocks[0]
                elif m == 'r':
                    print('rotate')
                    queue_blocks[0].short_shape = rotate_matrix(queue_blocks[0].short_shape)
                elif m == 'x':
                    x += 1
                    print('move', x)
                elif m == 'y':
                    print('hard drop')
                    y = best_move['y'] + 1
                pygame.time.set_timer(IA_TIMER, ia_delay)

        if not paused:
            #Select best option
            if not calculated:
                posibilites = list()
                posibilites.extend(gen_all_posibilites(0, queue_blocks[0], grid.shape))
                posibilites.extend(gen_all_posibilites(1, queue_blocks[1], grid.shape))
                posibilites = list(map(score_possibility, posibilites))
                posibilites = manual_selection(posibilites)
                # posibilites = [eval_possibility(posibilites[j], vector) for j in range(len(posibilites))] 
                # best_move = max(posibilites, key=lambda p: p['eval'])           
                best_move = posibilites
                auto_moves = move_to_key(best_move)
                print('')
                print(score, 'prediction', best_move['a'], best_move['turns'], best_move['moves'])
                print_grid(best_move['block'])
                calculated = True

            if check_collision(curr_block.short_shape, x, y, grid.shape):
                score += 1
                if score % 10 == 0:
                    # g = int(g * 0.9)
                    g -= 100
                merge_block3(curr_block, x, y, grid)
                queue_blocks.pop(0)
                fill_blocks(queue_blocks)
                full_rows = check_full_rows(grid.shape)
                if full_rows:
                    for row in full_rows:
                        remove_row(grid, row)
                score += len(full_rows)
                curr_block = queue_blocks[0]
                x, y = 0, 0
                calculated = False
                if check_collision(curr_block.short_shape, x, y, grid.shape):
                    draw_game_over()
                    pygame.display.update()
                    return


            # Draw game
            WIN.fill(BLACK)

            STATS.fill(BLACK)
            draw_stats_lines(STATS)
            draw_mode(STATS, mode)
            draw_next_block(STATS, queue_blocks[1])
            draw_scores(STATS, score, g, calculate_scores(grid.shape))
            WIN.blit(STATS, (400, 0))

            GAME.fill(BLACK)
            draw_grid_lines()
            draw_grid(grid)
            draw_block_n_prediction2(curr_block, x, y, grid.shape)
            WIN.blit(GAME, (0, 0))

            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    main()