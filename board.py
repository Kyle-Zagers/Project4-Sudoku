import pygame
from constants import *
from sudoku_generator import SudokuGenerator
from cell import Cell


class Board:
    cells = {}

    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height-75
        self.screen = screen
        self.removed = 0
        self.reset_rectangle = None
        self.restart_rectangle = None
        self.exit_rectangle = None
        match difficulty:
            case "easy":
                self.removed = 30
            case "medium":
                self.removed = 40
            case "hard":
                self.removed = 50

        self.sudoku = SudokuGenerator(9, self.removed)
        self.sudoku.fill_values()
        self.sudoku.remove_cells()
        self.board = self.sudoku.get_board()

        for column in range(9):
            self.cells[column] = {}
            for row in range(9):
                self.cells[column][row] = Cell(f"{self.board[column][row]}", row, column, screen)

    def draw(self):
        # draw horizontal lines
        for i in range(1, 3):
            pygame.draw.line(self.screen, LINE_COLOR, (0, SQUARE_SIZE * i),
                             (self.width, SQUARE_SIZE * i), BOLD_LINE_WIDTH)

            for i in range(1, 9):
                pygame.draw.line(self.screen, LINE_COLOR, (0, CELL_SIZE * i),
                                 (self.width, CELL_SIZE * i), THIN_LINE_WIDTH)
        # draw vertical lines
        for i in range(1, 3):
            pygame.draw.line(self.screen, LINE_COLOR, (SQUARE_SIZE * i, 0),
                             (SQUARE_SIZE * i, self.height), BOLD_LINE_WIDTH)

        for i in range(1, 9):
            pygame.draw.line(self.screen, LINE_COLOR, (CELL_SIZE * i, 0),
                             (CELL_SIZE * i, self.height), THIN_LINE_WIDTH)

        pygame.draw.line(self.screen, (0, 125, 200), (0, SQUARE_SIZE + 56 * 8),
                         (self.width, SQUARE_SIZE + 56 * 8), BOLD_LINE_WIDTH)

        for i in range(9):
            for j in range(9):
                self.cells[i][j].draw()

        # Initialize buttons
        # Initialize text first
        reset_text = BUTTON_FONT.render("Reset", True, (255, 255, 255))
        restart_text = BUTTON_FONT.render("Restart", True, (255, 255, 255))
        exit_text = BUTTON_FONT.render("Exit", True, (255, 255, 255))

        # Initialize the buttons' background color and text
        reset_surface = pygame.Surface((reset_text.get_size()[0] + 20, reset_text.get_size()[1] + 20))
        reset_surface.fill(LINE_COLOR)
        reset_surface.blit(reset_text, (10, 10))

        restart_surface = pygame.Surface((restart_text.get_size()[0] + 20, restart_text.get_size()[1] + 20))
        restart_surface.fill(LINE_COLOR)
        restart_surface.blit(restart_text, (10, 10))

        exit_surface = pygame.Surface((exit_text.get_size()[0] + 20, exit_text.get_size()[1] + 20))
        exit_surface.fill(LINE_COLOR)
        exit_surface.blit(exit_text, (10, 10))

        # Initialize button rectangles

        self.reset_rectangle = reset_surface.get_rect(center=(WIDTH // 4, HEIGHT // 2 + 338))
        self.restart_rectangle = restart_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 338))
        self.exit_rectangle = exit_surface.get_rect(center=((3 * WIDTH) // 4, HEIGHT // 2 + 338))

        # Draw buttons

        self.screen.blit(reset_surface, self.reset_rectangle)
        self.screen.blit(restart_surface, self.restart_rectangle)
        self.screen.blit(exit_surface, self.exit_rectangle)
