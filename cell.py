import pygame
from constants import *


class Cell:
    def __init__(self, value, row, col, screen):
        # Initializes the cell with various attributes.
        self.value = value
        self.sketched_value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.value_rect = None

    def set_cell_value(self, value):  # Setter for value.
        self.value = value

    def make_highlight(self):  # Makes a highlight of the current cell.
        pygame.draw.rect(self.screen, (255, 0, 0),
                         ((self.col * 75), (self.row * 75), CELL_SIZE+2, CELL_SIZE+2), 2)
        pygame.display.update()

    def delete_highlight(self):  # Gets rid of a highlight on the current cell.
        pygame.draw.rect(self.screen, LINE_COLOR,
                         ((self.col * 75), (self.row * 75), CELL_SIZE + 2, CELL_SIZE + 2), 2)
        pygame.draw.line(self.screen, (0, 125, 200), (0, SQUARE_SIZE + 56 * 8),
                         (WIDTH, SQUARE_SIZE + 56 * 8), BOLD_LINE_WIDTH)  # Redraws the line at the bottom for looks.
        pygame.display.update()

    # For both set_sketched_value() and draw(), blank is set to "      " so they can be clicked by the mouse.
    def set_sketched_value(self, sketched_value):  # Setting a sketched value.
        if self.value == "0":  # Can only set sketched values for cells without a given value.

            # Draws a rectangle in case of existing cell sketched value.
            pygame.draw.rect(self.screen, BG_COLOR, pygame.Rect((self.col * 75)+5, (self.row * 75)+5,
                                                                CELL_SIZE-10, CELL_SIZE-10))
            # Adding new sketched number.
            self.sketched_value = sketched_value
            value_font = pygame.font.Font(None, 60)
            # Pycharm didn't like the amount of characters.
            value_surf = value_font.render(
                f'{self.sketched_value if ord("1") <= ord(self.sketched_value) <= ord("9") else "      "}',
                True, LINE_COLOR)
            self.value_rect = value_surf.get_rect(
                center=(CELL_SIZE // 2 + CELL_SIZE * self.col, CELL_SIZE // 2 + CELL_SIZE * self.row))
            self.screen.blit(value_surf, self.value_rect)
            pygame.display.update()

    def draw(self):  # Draws the cell if it is given a non-zero value.
        value_font = pygame.font.Font(None, 60)
        value_surf = value_font.render(f'{self.value if ord("1")<=ord(self.value)<=ord("9") else "      "}', True,
                                       (255, 255, 255))
        self.value_rect = value_surf.get_rect(
            center=(CELL_SIZE // 2 + CELL_SIZE * self.col, CELL_SIZE // 2 + CELL_SIZE * self.row))

        # Draws the cells.
        pygame.draw.rect(self.screen, LINE_COLOR,
                         ((self.col * 75), (self.row * 75), CELL_SIZE + 2, CELL_SIZE + 2), 2)
        pygame.draw.line(self.screen, (0, 125, 200), (0, SQUARE_SIZE + 56 * 8),
                         (WIDTH, SQUARE_SIZE + 56 * 8), BOLD_LINE_WIDTH)

        self.screen.blit(value_surf, self.value_rect)

    # For representing the cell objects as various attributes in different use cases.
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return int(self.value)

    def __int__(self):
        return int(self.value)
