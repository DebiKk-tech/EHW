# Талдин М.
import pygame
import os
import sys
from constants import *


def load_image(name, colorkey=None):
    fullname = 'data/' + name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, groups, image):
        super().__init__()
        for group in groups:
            group.add(self)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Door(pygame.sprite.Sprite):
    def __init__(self, size, type, groups):
        super().__init__()
        self.image = load_image('maybeadoor.xcf')
        self.rect = self.image.get_rect()
        self.type = type
        for group in groups:
            group.add(self)
        if self.type == 'left':
            self.rect.x = SPACE
        else:
            self.rect.right = size[0] - SPACE
        self.rect.centery = size[1] // 2
        self.opened = True

    def set_opened(self):
        self.opened = True
        self.change_image('maybeadoor.xcf')

    def set_closed(self):
        self.opened = False
        self.change_image('locked_door.xcf')

    def change_image(self, name):
        coords = self.rect.center
        self.image = load_image(name)
        self.rect = self.image.get_rect()
        self.rect.center = coords
