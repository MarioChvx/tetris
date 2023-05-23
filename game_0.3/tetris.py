import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 400, 800
WIN = pygame.display.set_mode((WIDTH + 200, HEIGHT))
GAME = pygame.Surface((400, 800))
pygame.display.set_caption("Tetris")

# Define colors
BLACK   = pygame.Color(0,   0,   0,   255)
WHITE   = pygame.Color(255, 255, 255, 255)
RED     = pygame.Color(255, 0,   0,   255)
GREEN   = pygame.Color(0,   255, 0,   255)
BLUE    = pygame.Color(0,   0,   255, 255)
CYAN    = pygame.Color(0,   255, 255, 255)
MAGENTA = pygame.Color(255, 0,   255, 255)
YELLOW  = pygame.Color(255, 255, 0,   255)
ORANGE  = pygame.Color(255, 165, 0,   255)
GRAY    = pygame.Color(50,  50,  50,  255)

# Define shapes
I = [[0, 0, 0, 0],
     [1, 1, 1, 1],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]

O = [[1, 1],
     [1, 1]]

T = [[0, 1, 0],
     [1, 1, 1],
     [0, 0, 0]]

S = [[0, 1, 1],
     [1, 1, 0],
     [0, 0, 0]]

Z = [[1, 1, 0],
     [0, 1, 1],
     [0, 0, 0]]

J = [[1, 0, 0],
     [1, 1, 1],
     [0, 0, 0]]

L = [[0, 0, 1],
     [1, 1, 1],
     [0, 0, 0]]

# Define block shapes
SHAPES = [
    (I, CYAN),
    (O, YELLOW),
    (S, RED),
    (Z, GREEN),
    (T, MAGENTA),
    (J, BLUE),
    (L, ORANGE) 
]

# Define block size
BLOCK_SIZE = 40

# Calculate the number of blocks that fit the screen
GRID_WIDTH = WIDTH // BLOCK_SIZE
GRID_HEIGHT = HEIGHT // BLOCK_SIZE

# Timer for fall
FALL_SPEED = (7 * 1000) // 10  
FALL_TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(FALL_TIMER, FALL_SPEED)


def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(WIN, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(WIN, GRAY, (0, y), (WIDTH, y))


def draw_block(x, y, color):
    pygame.draw.rect(WIN, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def draw_prediction(x, y, color):
    pygame.draw.rect(WIN, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), BLOCK_SIZE // 12)


def create_block():
    return random.choice(SHAPES)
    # return SHAPES[0]


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
    for row in range(len(block)):
        for col in range(len(block[row])):
            if block[row][col]:
                grid[y + row - 1][x + col] = 1


def remove_row(grid, row):
    del grid[row]
    grid.insert(0, [0] * GRID_WIDTH)


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


def tetris():
    clock = pygame.time.Clock()
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    queue_blocks = create_blocks()
    curr_block, curr_color = queue_blocks[0]
    x, y = GRID_WIDTH // 2 - len(curr_block[0]) // 2, 0
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                prediction(curr_block, x, y, grid)
                if event.key in [pygame.K_LEFT, ord('a'), ord('A')]:
                    if not check_collision(curr_block, x - 1, y, grid):
                        x -= 1
                elif event.key in [pygame.K_RIGHT, ord('d'), ord('D')]:
                    if not check_collision(curr_block, x + 1, y, grid):
                        x += 1
                elif event.key in [pygame.K_DOWN, ord('s'), ord('S')]:
                    if not check_collision(curr_block, x, y + 1, grid):
                        y += 1
                elif event.key in [pygame.K_UP, ord('w'), ord('W')]:
                    rotated_block = list(zip(*reversed(curr_block)))
                    x = keep_in(rotated_block, x, y, grid)
                    curr_block = rotated_block
                elif event.key in [pygame.K_SPACE]:
                    p = prediction(curr_block, x, y, grid)
                    y = p
                elif event.key in [ord('h'), ord('H')]:
                    queue_blocks[0], queue_blocks[1] = queue_blocks[1], queue_blocks[0]
                    curr_block, curr_color = queue_blocks[0]
            
            if event.type == FALL_TIMER:
                y += 1
                pygame.time.set_timer(FALL_TIMER, FALL_SPEED - 1)
        
        if check_collision(curr_block, x, y, grid):
            merge_block(curr_block, x, y, grid)
            queue_blocks.pop(0)
            fill_blocks(queue_blocks)
            full_rows = check_full_rows(grid)
            if full_rows:
                for row in full_rows:
                    remove_row(grid, row)
                score += len(full_rows)
            curr_block, curr_color = queue_blocks[0]
            x, y = GRID_WIDTH // 2 - len(curr_block[0]) // 2, 0
            if check_collision(curr_block, x, y, grid):
                draw_game_over()
                pygame.display.update()
                return

        WIN.fill(BLACK)
        GAME.fill(BLACK)
        WIN.blit(GAME, (0, 0))
        pygame.draw.line(WIN, WHITE, (401, 0), (401, HEIGHT))
        pygame.draw.line(WIN, WHITE, (401, 160), (600, 160))
        c = (200 - 40 * len(queue_blocks[1][0])) // 2
        for row in range(len(queue_blocks[1][0])):
            for col in range(len(queue_blocks[1][0])):
                if queue_blocks[1][0][row][col]:
                    pygame.draw.rect(WIN, queue_blocks[1][1], (col * BLOCK_SIZE + 400 + c, row * BLOCK_SIZE + 40, BLOCK_SIZE, BLOCK_SIZE))

        draw_grid()

        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col]:
                    draw_block(col, row, WHITE)
        
        p = prediction(curr_block, x, y, grid)

        for row in range(len(curr_block)):
            for col in range(len(curr_block[row])):
                if curr_block[row][col]:
                    draw_prediction(x + col, p + row, curr_color)
                    draw_block(x + col, y + row, curr_color)

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    tetris()