
# The original Tetris game, but plays it self

My objectives for this project are:

1. Developing a functional copy of the game using Python.
2. Implementing a sort of AI that plays Tetris satisfactorily.

Currently...

## How I did it?

For the first objective I used Pygame, a library with a lot of useful features to build games with Python. I've learned a lot about Tetris it isn't as easy as it seems, things like the *soft rotation*, usually to rotate a matrix it's done by the corner doing it this way the animation look hard and weird but changing the pivot to the center improve a lot the looks of the game. Just like *soft rotation* are many more little details that I didn't notice until I started this project.

Right now the game is working just fine and has the principal attributes from the original game.

![normal game screenshot]()

I divided the game into two modes normal mode and AI mode, you can switch between them using F1 for normal mode and F2 for AI mode.

The AI is working for the first few pieces, but has some bugs that need a fixing and the code needs a clean up.
