# Талдин М.
import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, groups):
        super().__init__()
        for group in groups:
            group.add(self)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.image.fill((255, 255, 255))


class Door(pygame.sprite.Sprite):
    def __init__(self, size, type, groups):
        super().__init__()
        self.image = pygame.Surface((62, 102))
        self.image.fill((0, 255, 0))  #
        self.rect = self.image.get_rect()
        self.type = type
        for group in groups:
            group.add(self)
        if self.type == 'left':
            self.rect.x = 31
        else:
            self.rect.right = size[0] - 31
        self.rect.centery = size[1] // 2
        self.opened = True

    def set_opened(self):
        self.opened = True
        self.image = pygame.Surface((62, 102))
        self.image.fill((0, 255, 0))

    def set_closed(self):
        self.opened = False
        self.image = pygame.Surface((62, 102))
        self.image.fill((0, 255, 255))

    def change_image(self, name):
        coords = self.rect.center
        self.image = False
        self.rect = self.image.get_rect()
        self.rect.center = coords
