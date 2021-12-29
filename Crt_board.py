import pygame
from random import *


COLORS = ['black', 'green', 'black', 'black', 'brown', 'black', 'black', 'black', 'blue']


class Board:
    def __init__(self, width, height, left=10, top=10, cell_size=30):
        self.width = width
        self.height = height
        board_row = []
        self.board = []
        for i in range(height):
            for j in range(width):
                if i == 0 and j == 0 or i == height - 1 and j == 0 or i == 0 and j == width - 1 \
                    or i == height - 1 and j == width - 1:
                    board_row.append(randint(0, 1))
                elif i == 0 or i == height - 1:
                    board_row.append(randint(2, 4))
                elif abs(i - height // 2) <= 2 and abs(j - width / 2) <= 1:
                    board_row.append((randint(5, 8)))
                else:
                    board_row.append(0)
            self.board.append(board_row)
            board_row = []
        self.set_view(left, top, cell_size)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(screen, 'white', (self.left + col * self.cell_size,
                        self.top + row * self.cell_size, self.cell_size, self.cell_size), 1)

                pygame.draw.rect(screen, COLORS[self.board[row][col]], (self.left + col * self.cell_size + 1,
                                                                        self.top + row * self.cell_size + 1,
                                                                        self.cell_size - 2, self.cell_size - 2))


pygame.init()
size = wight, height = 1060, 560
screen = pygame.display.set_mode(size)
board = Board(20, 10, 30, 30, 50)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
pygame.quit()
