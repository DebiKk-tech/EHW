import pygame
from random import *
import os
import sys


COLORS = ['floor', 'plant', 'floor', 'floor', 'cupboard', 'floor', 'floor', 'floor', 'table']
all_sprites = pygame.sprite.Group()
furniture_sprites = pygame.sprite.Group()
plant_sprites = pygame.sprite.Group()
surf = pygame.Surface((1060, 560))


def load_image(name, colorkey=None):
    fullname = 'data/' + name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

# Костя К
class floor(pygame.sprite.Sprite):
    def __init__(self, image_name, x, y):
        super().__init__(all_sprites)
        self.image = load_image(image_name)
        self.rect = self.image.get_rect()
        self.cur_frame = 0
        self.rect = self.rect.move(x, y)

    def update(self):
        pass

    # никак не взаимодействует - поэтому нет коллизии


class plant_sprite(pygame.sprite.Sprite):
    def __init__(self, image_name, x, y):
        super().__init__(plant_sprites)
        self.image = load_image(image_name)
        self.rect = self.image.get_rect()
        self.cur_frame = 0
        self.rect = self.rect.move(x, y)

    def update(self):
        pass

    def collision(self, object):
        # предполагаю, что растение будет менять текстуру на разбитую при столкновении с пулей
        pass


class furniture_sprite(pygame.sprite.Sprite):
    def __init__(self, image_name, x, y):
        super().__init__(furniture_sprites)
        self.image = load_image(image_name)
        self.rect = self.image.get_rect()
        self.cur_frame = 0
        self.rect = self.rect.move(x, y)

    def update(self):
        pass

    def collision(self, object):
        pass

# -----------------
class Board:
    def __init__(self, width, height, left=30, top=30, cell_size=50, board=[]):
        # Cаша Ч
        self.width = width
        self.height = height
        board_row = []
        self.board = board
        if board == []:
            for i in range(height):
                for j in range(width):
                    if i == 0 and j == 0 or i == height - 1 and j == 0 or i == 0 and j == width - 1 \
                        or i == height - 1 and j == width - 1:
                        board_row.append(randint(0, 1))
                    elif i == 0 or i == height - 1:
                        board_row.append(randint(2, 5))
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

    def ret_board(self):
        return self.board

    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                #костя К. + ал. ч(немного видоизменил)
                pygame.draw.rect(screen, 'black', (self.left + col * self.cell_size,
                        self.top + row * self.cell_size, self.cell_size, self.cell_size), 1)
                if self.board[row][col] == 'cupboard':
                    current_object = furniture_sprite('cupboard.xcf', self.left + col * self.cell_size + 1,
                                                                        self.top + row * self.cell_size + 1)
                elif self.board[row][col] == 'floor':
                    current_object = floor('floor.xcf', self.left + col * self.cell_size + 1,
                                                   self.top + row * self.cell_size + 1)
                elif self.board[row][col] == 'table':
                    current_object = furniture_sprite('table.xcf', self.left + col * self.cell_size + 1,
                                                   self.top + row * self.cell_size + 1)
                elif self.board[row][col] == 'plant':
                    current_object = plant_sprite('plant.xcf', self.left + col * self.cell_size + 1,
                                                   self.top + row * self.cell_size + 1)
        furniture_sprites.draw(screen)
        plant_sprites.draw(screen)
        all_sprites.draw(screen)


# Ал. Ч(нововведение)
def main(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            board[row][col] = COLORS[board[row][col]]
    return Board(len(board[0]), len(board), board=board)
# ----


pygame.init()
size = wight, height = 1060, 560
screen = pygame.display.set_mode(size)
board = main(Board(20, 10, 30, 30, 50).ret_board())
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
pygame.quit()
