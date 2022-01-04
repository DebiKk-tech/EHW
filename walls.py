# Талдин М.
import pygame
from spawn_living import *


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, groups):
        super().__init__()
        for group in groups:
            group.add(self)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.image.fill((255, 255, 255))
