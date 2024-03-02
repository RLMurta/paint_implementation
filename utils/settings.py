import pygame

pygame.init()
pygame.font.init()

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)

# Game frame rate
FPS = 120

# Window Settings
WIDTH, HEIGHT = 600, 700

# Grid Settings
ROWS = COLS = 50

# Toolbar Settings
TOOLBAR_HEIGHT = HEIGHT - WIDTH

# Drawing Settings
PIXEL_SIZE = WIDTH // COLS

# Background Color
BG_COLOR = WHITE

DRAW_GRID_LINES = True

def get_font(size):
    return pygame.font.SysFont("comicsans", size)