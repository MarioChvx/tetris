import pygame
import random
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

def draw_scores(surf, score, gravity):
    font = pygame.font.Font(None, 36)
    punctuation = font.render(f'BLOCKS: {score}', True, WHITE)
    surf.blit(punctuation, (10, 210))
    punctuation = font.render(f'SPEED: {(1 / gravity) * 1000} B/s', True, WHITE)
    surf.blit(punctuation, (10, 260))


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
    max_y, min_y = 0, 0
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


def merge_block(block, x, y, grid):
    n = len(block.shape)
    for row in range(n):
        for col in range(n):
            if block.shape[row][col]:
                pass
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


def draw_game_over():
    font = pygame.font.Font(None, 64)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.blit(text, text_rect)


def prediction(block, x, y, grid):
    block_bottom = list()
    for col in range(len(block[0])):
        block_bottom.append(-1)
        for row in range(len(block)):
            if row > block_bottom[-1] and block[row][col]:
                block_bottom[-1] = row
    
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

    return  min([grid_top[i] - block_bottom[i] - 1 for i in range(len(grid_top))])


def new_matrix(i, j, fill=0):
    res = list()
    for row in range(i):
        res.append([fill] * j)
    return res


def print_grid(grid):
    print('')
    for row in grid:
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


def tetris():
    g = 1000
    pygame.time.set_timer(FALL_TIMER, g)
    clock = pygame.time.Clock()
    grid = Grid(new_matrix(GRID_HEIGHT, GRID_WIDTH), new_matrix(GRID_HEIGHT, GRID_WIDTH, None))
    queue_blocks = create_blocks()
    curr_block = queue_blocks[0]
    x, y = GRID_WIDTH // 2 - len(curr_block.shape) // 2, 0
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                x, y = check_movement(event, x, y, queue_blocks, grid.shape)
                curr_block = queue_blocks[0]

            if event.type == FALL_TIMER:
                y += 1
                pygame.time.set_timer(FALL_TIMER, g)
        
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
        draw_next_block(STATS, queue_blocks[1])
        draw_scores(STATS, score, g)
        WIN.blit(STATS, (400, 0))

        GAME.fill(BLACK)
        draw_grid_lines()
        draw_grid(grid)
        draw_block_n_prediction(curr_block, x, y, grid.shape)
        WIN.blit(GAME, (0, 0))

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    tetris()