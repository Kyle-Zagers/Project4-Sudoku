import sys
from constants import *
from board import Board
import pygame


def start_screen(screen):  # Creates the start screen for the game.
    pygame.display.set_caption("Sudoku")

    # Color background.
    screen.fill(BG_COLOR)

    # Initialize and draw title.
    title_surface = TITLE_FONT.render("Welcome to Sudoku", True, LINE_COLOR)
    title_rectangle = title_surface.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 175))
    screen.blit(title_surface, title_rectangle)

    title_surface2 = TITLE_FONT_2.render("Select Game Mode:", True, LINE_COLOR)
    title_rectangle2 = title_surface2.get_rect(
        center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(title_surface2, title_rectangle2)

    # Initialize buttons.
    easy_text = BUTTON_FONT.render("Easy", True, (255, 255, 255))
    medium_text = BUTTON_FONT.render("Medium", True, (255, 255, 255))
    hard_text = BUTTON_FONT.render("Hard", True, (255, 255, 255))

    # Initialize the buttons' background color and text.
    easy_surface = pygame.Surface((easy_text.get_size()[0] + 20, easy_text.get_size()[1] + 20))
    easy_surface.fill(LINE_COLOR)
    easy_surface.blit(easy_text, (10, 10))

    medium_surface = pygame.Surface((medium_text.get_size()[0] + 20, medium_text.get_size()[1] + 20))
    medium_surface.fill(LINE_COLOR)
    medium_surface.blit(medium_text, (10, 10))

    hard_surface = pygame.Surface((hard_text.get_size()[0] + 20, hard_text.get_size()[1] + 20))
    hard_surface.fill(LINE_COLOR)
    hard_surface.blit(hard_text, (10, 10))

    # Initialize button rectangles.
    easy_rectangle = easy_surface.get_rect(center=(WIDTH // 4, HEIGHT // 2 + 100))
    medium_rectangle = medium_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    hard_rectangle = hard_surface.get_rect(center=((3 * WIDTH) // 4, HEIGHT // 2 + 100))

    # Draw buttons
    screen.blit(easy_surface, easy_rectangle)
    screen.blit(medium_surface, medium_rectangle)
    screen.blit(hard_surface, hard_rectangle)

    # Gets input from the user.
    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.MOUSEBUTTONDOWN:
                    if easy_rectangle.collidepoint(event.pos):  # Easy removes 30 cells
                        return 30
                    if medium_rectangle.collidepoint(event.pos):  # Medium removes 40 cells
                        return 40
                    if hard_rectangle.collidepoint(event.pos):  # Hard removes 50 cells
                        return 50
        pygame.display.update()


def won_exit_screen(screen):  # Screen that is displayed if the user won.
    # Color background
    screen.fill(BG_COLOR)

    # Initialize and draw title
    title_surface = TITLE_FONT.render("Game Won!", True, LINE_COLOR)
    title_rectangle = title_surface.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 175))
    screen.blit(title_surface, title_rectangle)

    # Initialize the button's background color and text.
    won_text = BUTTON_FONT.render("Exit", True, (255, 255, 255))
    won_surface = pygame.Surface((won_text.get_size()[0] + 20, won_text.get_size()[1] + 20))
    won_surface.fill(LINE_COLOR)
    won_surface.blit(won_text, (10, 10))
    # Initializes button rectangles.
    won_rectangle = won_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    # Draws the button.
    screen.blit(won_surface, won_rectangle)

    # Gets user input.
    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.MOUSEBUTTONDOWN:  # Exits program.
                    if won_rectangle.collidepoint(event.pos):
                        sys.exit()
                case pygame.QUIT:
                    sys.exit()
        pygame.display.update()


def loss_exit_screen(screen):  # Screen that is displayed if the user lost.
    # Color background
    screen.fill(BG_COLOR)

    # Initialize and draw title
    title_surface = TITLE_FONT.render("Game Over :(", False, LINE_COLOR)
    title_rectangle = title_surface.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 175))
    screen.blit(title_surface, title_rectangle)

    # Initialize the button's background color and text.
    loss_text = BUTTON_FONT.render("Restart", False, (255, 255, 255))
    loss_surface = pygame.Surface((loss_text.get_size()[0] + 20, loss_text.get_size()[1] + 20))
    loss_surface.fill(LINE_COLOR)
    loss_surface.blit(loss_text, (10, 10))
    # Initializes button rectangles.
    loss_rectangle = loss_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    # Draws the button.
    screen.blit(loss_surface, loss_rectangle)

    # Gets user input.
    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.MOUSEBUTTONDOWN:
                    if loss_rectangle.collidepoint(event.pos):  # Restarts program.
                        main()
                case pygame.QUIT:
                    sys.exit()
        pygame.display.update()


def game_buttons(board, screen, event, mode):  # Buttons for when the game is being played.
    result = True
    if board.reset_rectangle.collidepoint(event.pos):  # Reset button resets the board.
        screen.fill(BG_COLOR)
        board = Board(WIDTH, HEIGHT, screen, mode)
        board.draw()
        pygame.display.update()
    elif board.restart_rectangle.collidepoint(event.pos):  # Restart button takes you back to the start screen.
        main()
    elif board.exit_rectangle.collidepoint(event.pos):  # Exits the program.
        sys.exit()
    else:
        result = False
    return [result, board]  # Returns if a button was pressed and the board with changes.


def has_won(screen, board):
    won = True
    for x in range(9):
        for y in range(9):
            # Has to remove the value to check if that value can go there.
            board.sudoku.board[x][y] = 0
            if not board.sudoku.is_valid(x, y, board.cells[x][y].sketched_value):  # Checks if valid.
                won = False
            board.sudoku.board[x][y] = board.cells[x][y].sketched_value  # Re-adds the value for future checks.

            if board.cells[x][y].value == "0" and board.cells[x][y].sketched_value == 0:  # Verifies the user inputted.
                won = False
    if won:
        won_exit_screen(screen)
    else:
        loss_exit_screen(screen)


def number_input(board, row, col, key):  # Inputs the entered value into the board 2d list and the UI board.
    board.cells[row][col].set_sketched_value(f"{key}")
    board.sudoku.board[row][col] = key


def main():
    pygame.init()  # Initializes pygame.
    screen = pygame.display.set_mode([WIDTH, HEIGHT])  # Creates the window.
    removed = start_screen(screen)  # Shows the start screen and gets the number of removed cells.
    screen.fill(BG_COLOR)  # Makes the background.

    # Draws the board with random values.
    board = Board(WIDTH, HEIGHT, screen, removed)
    board.draw()
    pygame.display.update()

    # Checks for user input.
    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.KEYDOWN:  # If enter is pressed then it checks if the user won.
                    if event.key == pygame.K_RETURN:
                        has_won(screen, board)
                        break
                case pygame.MOUSEBUTTONDOWN:  # If the user clicks.
                    buttons = game_buttons(board, screen, event, removed)
                    board = buttons[1]
                    if not buttons[0]:  # If the user didn't click on one of the buttons at the bottom.
                        # Checks which cell they clicked on.
                        for row in board.cells:
                            for col in board.cells[row]:
                                if board.cells[row][col].value_rect.collidepoint(event.pos)\
                                        and board.cells[row][col].value == "0":  # Only allows change if cell is empty.
                                    go = True
                                    while go:  # Checks for user input.
                                        board.cells[row][col].make_highlight()  # Highlights the current cell.
                                        for event2 in pygame.event.get():
                                            if event2.type == pygame.KEYDOWN:  # If keyboard button pressed.
                                                match event2.key:
                                                    # Moves the highlighted cell in inputted direction if possible.
                                                    case pygame.K_DOWN:
                                                        board.cells[row][col].delete_highlight()
                                                        col += 1 if col != 8 else 0
                                                    case pygame.K_UP:
                                                        board.cells[row][col].delete_highlight()
                                                        col -= 1 if col != 0 else 0
                                                    case pygame.K_RIGHT:
                                                        board.cells[row][col].delete_highlight()
                                                        row += 1 if row != 8 else 0
                                                    case pygame.K_LEFT:
                                                        board.cells[row][col].delete_highlight()
                                                        row -= 1 if row != 0 else 0

                                                    # Checks for digit input for cell.
                                                    case pygame.K_1:
                                                        number_input(board, row, col, 1)
                                                        go = False
                                                        break
                                                    case pygame.K_2:
                                                        number_input(board, row, col, 2)
                                                        go = False
                                                        break
                                                    case pygame.K_3:
                                                        number_input(board, row, col, 3)
                                                        go = False
                                                        break
                                                    case pygame.K_4:
                                                        number_input(board, row, col, 4)
                                                        go = False
                                                        break
                                                    case pygame.K_5:
                                                        number_input(board, row, col, 5)
                                                        go = False
                                                        break
                                                    case pygame.K_6:
                                                        number_input(board, row, col, 6)
                                                        go = False
                                                        break
                                                    case pygame.K_7:
                                                        number_input(board, row, col, 7)
                                                        go = False
                                                        break
                                                    case pygame.K_8:
                                                        number_input(board, row, col, 8)
                                                        go = False
                                                        break
                                                    case pygame.K_9:
                                                        number_input(board, row, col, 9)
                                                        go = False
                                                        break
                                            if event2.type == pygame.QUIT:
                                                sys.exit()
                                            if event2.type == pygame.MOUSEBUTTONDOWN:  # Checks if button was pressed.
                                                board = game_buttons(board, screen, event2, removed)[1]
                                    board.cells[row][col].delete_highlight()  # Removes the highlight when done.


if __name__ == "__main__":  # Runs the main method.
    main()
