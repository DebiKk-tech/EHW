import pygame
from random import *
import os
import sys


COLORS = ['floor', 'plant', 'floor', 'floor', 'cupboard', 'floor', 'floor', 'floor', 'table']
all_sprites = pygame.sprite.Group()
surf = pygame.Surface((1060, 560))


def load_image(name, colorkey=None):
    fullname = "data/" + name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


main_image = load_image('main_surface.xcf')



class object_sprite(pygame.sprite.Sprite):
    def __init__(self, image_name, x, y):
        super().__init__(all_sprites)
        self.image = load_image(image_name)
        self.rect = self.image.get_rect()
        self.cur_frame = 0
        self.rect = self.rect.move(x, y)

    def update(self):
        pass


class Board:
    def __init__(self, width, height, left=10, top=10, cell_size=30):
        # Cаша Ч
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
                #костя К.
                pygame.draw.rect(screen, 'black', (self.left + col * self.cell_size,
                        self.top + row * self.cell_size, self.cell_size, self.cell_size), 1)
                if COLORS[self.board[row][col]] == 'cupboard':
                    current_object = object_sprite('cupboard.xcf', self.left + col * self.cell_size + 1,
                                                                        self.top + row * self.cell_size + 1)
                elif COLORS[self.board[row][col]] == 'floor':
                    current_object = object_sprite('floor.xcf', self.left + col * self.cell_size + 1,
                                                   self.top + row * self.cell_size + 1)
                elif COLORS[self.board[row][col]] == 'table':
                    current_object = object_sprite('table.xcf', self.left + col * self.cell_size + 1,
                                                   self.top + row * self.cell_size + 1)
                elif COLORS[self.board[row][col]] == 'plant':
                    current_object = object_sprite('plant.xcf', self.left + col * self.cell_size + 1,
                                                   self.top + row * self.cell_size + 1)
                    current_object = object_sprite('hero_end.xcf', self.left + col * self.cell_size + 1,
                                                   self.top + row * self.cell_size + 1)
        all_sprites.draw(screen)


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
