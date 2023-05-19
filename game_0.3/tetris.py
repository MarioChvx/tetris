import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 400, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (50, 50, 50)

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
FALL_SPEED = 1 * 1000
FALL_TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(FALL_TIMER, FALL_SPEED)

def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(WIN, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(WIN, GRAY, (0, y), (WIDTH, y))

def draw_block(x, y, color):
    pygame.draw.rect(WIN, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def create_block():
    return random.choice(SHAPES)
    # return SHAPES[0]

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
                max_y = max_y if max_y > row else row
                min_x = min_x if min_x < col else col
                min_y = min_y if min_y < row else row
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

def tetris():
    clock = pygame.time.Clock()
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    curr_block, curr_color = create_block()
    x, y = GRID_WIDTH // 2 - len(curr_block[0]) // 2, 0
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
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
            
            if event.type == FALL_TIMER:
                y += 1
                pygame.time.set_timer(FALL_TIMER, FALL_SPEED - 1)
        
        if check_collision(curr_block, x, y, grid):
            merge_block(curr_block, x, y, grid)
            full_rows = check_full_rows(grid)
            if full_rows:
                for row in full_rows:
                    remove_row(grid, row)
                score += len(full_rows)
            curr_block, curr_color = create_block()
            x, y = GRID_WIDTH // 2 - len(curr_block[0]) // 2, 0
            if check_collision(curr_block, x, y, grid):
                draw_game_over()
                pygame.display.update()
                return

        WIN.fill(BLACK)
        draw_grid()

        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col]:
                    draw_block(col, row, WHITE)

        for row in range(len(curr_block)):
            for col in range(len(curr_block[row])):
                if curr_block[row][col]:
                    draw_block(x + col, y + row, curr_color)

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    tetris()