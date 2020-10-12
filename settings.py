import sys
# This file contains constants used for the game 

# DEBUG MODE ON?
DEBUG = True
STYLE = True

# Check System
if sys.platform in ["win32", "win64"]:
    SYSTEM = True
else:
    SYSTEM = False

# Screen and Game size
WIDTH = 560
HEIGHT = 740

HEIGHTBUFFER = 60 

ROWS = 37
COLUMNS = 28

GAMEWIDTH = WIDTH
GAMEHEIGHT = HEIGHT-HEIGHTBUFFER*2

CELLWIDTH = int(GAMEWIDTH/COLUMNS)
CELLHEIGHT = int(GAMEHEIGHT/(ROWS-6))

FPS = 60

PLAYERRADIUS = 10

# Colours 
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 184, 82)

YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game Settings
BONUSLIFE = 10000   # The point intervals that the player recieves a bonus life at