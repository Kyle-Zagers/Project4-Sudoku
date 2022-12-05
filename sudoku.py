import sys
from constants import *
from board import Board
import pygame


def start_screen(screen):
    pygame.display.set_caption("Sudoku")

    # Color background
    screen.fill(BG_COLOR)

    # Initialize and draw title
    title_surface = TITLE_FONT.render("Welcome to Sudoku", True, LINE_COLOR)
    title_rectangle = title_surface.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 175))
    screen.blit(title_surface, title_rectangle)

    title_surface2 = TITLE_FONT_2.render("Select Game Mode:", True, LINE_COLOR)
    title_rectangle2 = title_surface2.get_rect(
        center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(title_surface2, title_rectangle2)

    # Initialize buttons
    # Initialize text first
    easy_text = BUTTON_FONT.render("Easy", True, (255, 255, 255))
    medium_text = BUTTON_FONT.render("Medium", True, (255, 255, 255))
    hard_text = BUTTON_FONT.render("Hard", True, (255, 255, 255))

    # Initialize the buttons' background color and text
    easy_surface = pygame.Surface((easy_text.get_size()[0] + 20, easy_text.get_size()[1] + 20))
    easy_surface.fill(LINE_COLOR)
    easy_surface.blit(easy_text, (10, 10))

    medium_surface = pygame.Surface((medium_text.get_size()[0] + 20, medium_text.get_size()[1] + 20))
    medium_surface.fill(LINE_COLOR)
    medium_surface.blit(medium_text, (10, 10))

    hard_surface = pygame.Surface((hard_text.get_size()[0] + 20, hard_text.get_size()[1] + 20))
    hard_surface.fill(LINE_COLOR)
    hard_surface.blit(hard_text, (10, 10))

    # Initialize button rectangles

    easy_rectangle = easy_surface.get_rect(center=(WIDTH // 4, HEIGHT // 2 + 100))
    medium_rectangle = medium_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    hard_rectangle = hard_surface.get_rect(center=((3 * WIDTH) // 4, HEIGHT // 2 + 100))

    # Draw buttons

    screen.blit(easy_surface, easy_rectangle)
    screen.blit(medium_surface, medium_rectangle)
    screen.blit(hard_surface, hard_rectangle)

    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.MOUSEBUTTONDOWN:
                    if easy_rectangle.collidepoint(event.pos):
                        return "easy"
                    if medium_rectangle.collidepoint(event.pos):
                        return "medium"
                    if hard_rectangle.collidepoint(event.pos):
                        return "hard"
        pygame.display.update()


def won_exit_screen(screen):
    # Initialize title font
    start_title_font = pygame.font.Font(None, 90)
    start_title2_font = pygame.font.Font(None, 66)
    button_font = pygame.font.Font(None, 50)

    # Color background
    screen.fill(BG_COLOR)

    # Initialize and draw title
    title_surface = start_title_font.render("Game Won!", True, LINE_COLOR)
    title_rectangle = title_surface.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 175))
    screen.blit(title_surface, title_rectangle)

    won_text = button_font.render("Exit", True, (255, 255, 255))
    won_surface = pygame.Surface((won_text.get_size()[0] + 20, won_text.get_size()[1] + 20))
    won_surface.fill(LINE_COLOR)
    won_surface.blit(won_text, (10, 10))
    won_rectangle = won_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(won_surface, won_rectangle)

    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.MOUSEBUTTONDOWN:
                    if won_rectangle.collidepoint(event.pos):
                        sys.exit()
                case pygame.QUIT:
                    sys.exit()
        pygame.display.update()


def loss_exit_screen(screen):
    # Initialize title font
    start_title_font = pygame.font.Font(None, 90)
    start_title2_font = pygame.font.Font(None, 66)
    button_font = pygame.font.Font(None, 50)

    # Color background
    screen.fill(BG_COLOR)

    # Initialize and draw title
    title_surface = start_title_font.render("Game Over :(", False, LINE_COLOR)
    title_rectangle = title_surface.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 175))
    screen.blit(title_surface, title_rectangle)

    loss_text = button_font.render("Restart", False, (255, 255, 255))
    loss_surface = pygame.Surface((loss_text.get_size()[0] + 20, loss_text.get_size()[1] + 20))
    loss_surface.fill(LINE_COLOR)
    loss_surface.blit(loss_text, (10, 10))
    loss_rectangle = loss_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(loss_surface, loss_rectangle)

    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.MOUSEBUTTONDOWN:
                    if loss_rectangle.collidepoint(event.pos):
                        main()
                case pygame.QUIT:
                    sys.exit()
        pygame.display.update()


def has_won(screen, board):
    won = True
    for x in range(9):
        for y in range(9):
            if board.cells[x][y].value == "0" and board.cells[x][y].sketched_value == 0:
                won = False
    if won:
        won_exit_screen(screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    mode = start_screen(screen)
    screen.fill(BG_COLOR)

    board = Board(WIDTH, HEIGHT, screen, mode)
    board.draw()
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.MOUSEBUTTONDOWN:
                    if board.reset_rectangle.collidepoint(event.pos):
                        screen.fill(BG_COLOR)
                        board = Board(WIDTH, HEIGHT, screen, mode)
                        board.draw()
                        pygame.display.update()
                    elif board.restart_rectangle.collidepoint(event.pos):
                        main()
                    elif board.exit_rectangle.collidepoint(event.pos):
                        sys.exit()
                    else:
                        for row in board.cells:
                            for col in board.cells[row]:
                                if board.cells[row][col].value_rect.collidepoint(event.pos) and board.cells[row][col].value == "0":
                                    not_lose = False
                                    for i in range(9):
                                        if board.sudoku.is_valid(row, col, i+1):
                                            not_lose = True
                                            break
                                    if not not_lose:
                                        loss_exit_screen(screen)
                                    go = True
                                    while go:
                                        for event2 in pygame.event.get():
                                            if event2.type == pygame.KEYDOWN:
                                                if event2.key == pygame.K_1:
                                                    if board.sudoku.is_valid(row, col, 1):
                                                        board.cells[row][col].set_sketched_value("1")
                                                        board.sudoku.board[row][col] = 1
                                                        go = False
                                                        break
                                                if event2.key == pygame.K_2:
                                                    if board.sudoku.is_valid(row, col, 2):
                                                        board.cells[row][col].set_sketched_value("2")
                                                        board.sudoku.board[row][col] = 2
                                                        go = False
                                                        break
                                                if event2.key == pygame.K_3:
                                                    if board.sudoku.is_valid(row, col, 3):
                                                        board.cells[row][col].set_sketched_value("3")
                                                        board.sudoku.board[row][col] = 3
                                                        go = False
                                                        break
                                                if event2.key == pygame.K_4:
                                                    if board.sudoku.is_valid(row, col, 4):
                                                        board.cells[row][col].set_sketched_value("4")
                                                        board.sudoku.board[row][col] = 4
                                                        go = False
                                                        break
                                                if event2.key == pygame.K_5:
                                                    if board.sudoku.is_valid(row, col, 5):
                                                        board.cells[row][col].set_sketched_value("5")
                                                        board.sudoku.board[row][col] = 5
                                                        go = False
                                                        break
                                                if event2.key == pygame.K_6:
                                                    if board.sudoku.is_valid(row, col, 6):
                                                        board.cells[row][col].set_sketched_value("6")
                                                        board.sudoku.board[row][col] = 6
                                                        go = False
                                                        break
                                                if event2.key == pygame.K_7:
                                                    if board.sudoku.is_valid(row, col, 7):
                                                        board.cells[row][col].set_sketched_value("7")
                                                        board.sudoku.board[row][col] = 7
                                                        go = False
                                                        break
                                                if event2.key == pygame.K_8:
                                                    if board.sudoku.is_valid(row, col, 8):
                                                        board.cells[row][col].set_sketched_value("8")
                                                        board.sudoku.board[row][col] = 8
                                                        go = False
                                                        break
                                                if event2.key == pygame.K_9:
                                                    if board.sudoku.is_valid(row, col, 9):
                                                        board.cells[row][col].set_sketched_value("9")
                                                        board.sudoku.board[row][col] = 9
                                                        go = False
                                                        break
                                            if event2.type == pygame.QUIT:
                                                sys.exit()
                                            if event2.type == pygame.MOUSEBUTTONDOWN:
                                                if board.reset_rectangle.collidepoint(event2.pos):
                                                    screen.fill(BG_COLOR)
                                                    board = Board(WIDTH, HEIGHT, screen, mode)
                                                    board.draw()
                                                    pygame.display.update()
                                                elif board.restart_rectangle.collidepoint(event2.pos):
                                                    main()
                                                elif board.exit_rectangle.collidepoint(event2.pos):
                                                    sys.exit()
                                    has_won(screen, board)

                case pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        print("reset")
                        # for resetting the game when "r" pressed.


if __name__ == "__main__":
    main()
