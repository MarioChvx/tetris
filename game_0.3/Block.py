from dataclasses import dataclass
from pygame import Color
import pygame 

# Define colors
# Define colors
BLACK   = pygame.Color(0,   0,   0,   255)
WHITE   = pygame.Color(255, 255, 255, 255)
GRAY    = pygame.Color(50,  50,  50,  255)

RED     = pygame.Color(255, 0,   0,   255)
GREEN   = pygame.Color(0,   255, 0,   255)
BLUE    = pygame.Color(0,   0,   255, 255)
CYAN    = pygame.Color(0,   255, 255, 255)
MAGENTA = pygame.Color(255, 0,   255, 255)
YELLOW  = pygame.Color(255, 255, 0,   255)
ORANGE  = pygame.Color(255, 165, 0,   255)

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

# Define short shapes
i = [[1, 1, 1, 1]]

t = [[0, 1, 0],
     [1, 1, 1]]

s = [[0, 1, 1],
     [1, 1, 0]]

z = [[1, 1, 0],
     [0, 1, 1]]

j = [[1, 0, 0],
     [1, 1, 1]]

l = [[0, 0, 1],
     [1, 1, 1]]


@dataclass
class Block:
    shape: tuple
    short_shape: tuple
    color: Color
    turns: int

blocks = (
    Block(O, O, YELLOW,  1),
    Block(I, i, CYAN,    2),
    Block(S, s, RED,     2),
    Block(Z, z, GREEN,   2),
    Block(T, t, MAGENTA, 4),
    Block(J, j, BLUE,    4),
    Block(L, l, ORANGE,  4) 
)