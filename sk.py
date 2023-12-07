import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 450, 450
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initial Sudoku board (0 represents an empty cell)
initial_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Create a copy of the board to store the current state
board = [row[:] for row in initial_board]

# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")

# Function to draw the Sudoku grid
def draw_grid():
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)

# Function to draw the Sudoku numbers
def draw_numbers():
    font = pygame.font.Font(None, 36)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if initial_board[i][j] != 0:
                text = font.render(str(initial_board[i][j]), True, BLACK)
                text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)
            elif board[i][j] != 0:
                text = font.render(str(board[i][j]), True, RED)
                text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

# Function to check if a number is valid in a given position
def is_valid(num, row, col):
    # Check row and column
    if num in board[row] or num in [board[i][col] for i in range(GRID_SIZE)]:
        return False

    # Check 3x3 subgrid
    subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
    return num not in [board[i][j] for i in range(subgrid_row, subgrid_row + 3) for j in range(subgrid_col, subgrid_col + 3)]

# Function to solve the Sudoku using backtracking
def solve():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0:
                for num in range(1, GRID_SIZE + 1):
                    if is_valid(num, i, j):
                        board[i][j] = num
                        if solve():
                            return True
                        board[i][j] = 0  # Backtrack if the current configuration is not valid
                return False
    return True

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                solve()

    screen.fill(WHITE)
    draw_grid()
    draw_numbers()

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
