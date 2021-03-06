import pygame
from player import *
from random import *
import os
import sys
from constants import *


all_sprites = pygame.sprite.Group()
furniture_sprites = pygame.sprite.Group()
plant_sprites = pygame.sprite.Group()


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


# -----------------


class Board:
    def __init__(self, width, height):
        # Cаша Ч
        self.width = width
        self.height = height
        board_row = []
        self.board = []
        for i in range(height):
            for j in range(width):
                if i == 0 and j == 0 or i == height - 1 and j == 0 or i == 0 and j == width - 1 \
                         or i == height - 1 and j == width - 1:
                    board_row.append(COLORS[randint(0, 1)])
                elif i == 0 or i == height - 1:
                    board_row.append(COLORS[randint(2, 5)])
                elif abs(i - height // 2) <= 2 and abs(j - width / 2) <= 1:
                    board_row.append((COLORS[randint(5, 8)]))
                else:
                    board_row.append(COLORS[0])
            self.board.append(board_row)
            board_row = []
        self.board[height // 2 - 1][0] = self.board[height // 2][0] = self.board[height // 2 - 1][width - 1] =\
            self.board[height // 2][width - 1] = COLORS[9]
        self.set_view(LEFT, TOP, CELL_SIZE)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for row in range(self.height):
            for col in range(self.width):
                #костя К.
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


def main(boards, cur_ind):
    return boards[cur_ind]


def get_decorate():
    return all_sprites, plant_sprites, furniture_sprites


boards = []
cur_ind = 0
board = Board(20, 10)
boards.append(board)
cur_board = main(boards, cur_ind)
cur_board.render()