import pygame

# Width and Height of the window.
WIDTH = 675
HEIGHT = 750

# Size of one of the 81 cells and size of one of the 9 cell groupings.
CELL_SIZE = 75
SQUARE_SIZE = 225

# Background color and color of the lines.
BG_COLOR = (0, 150, 200)
LINE_COLOR = (245, 152, 66)

# Width of the bold and thin lines.
BOLD_LINE_WIDTH = 6
THIN_LINE_WIDTH = 2

# Fonts used in the game.
pygame.font.init()
TITLE_FONT = pygame.font.Font(None, 90)
TITLE_FONT_2 = pygame.font.Font(None, 66)
BUTTON_FONT = pygame.font.Font(None, 50)
