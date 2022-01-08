import pygame
from pygame.constants import *
import os

pygame.init()
size = width, height = 1000, 560
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()


class RedactorSprite(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__(all_sprites)
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.type = type


class Player(RedactorSprite):
    def __init__(self, pos, type):
        super().__init__(pos, type)
        self.image.fill((0, 0, 255))


class CommonEnemy(RedactorSprite):
    def __init__(self, pos, type):
        super().__init__(pos, type)
        self.image.fill((220, 20, 60))


class ShootingEnemy(RedactorSprite):
    def __init__(self, pos, type):
        super().__init__(pos, type)
        self.image.fill((255, 255, 0))


class Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((100, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (890, 510)


def save_into_file():
    name = 'levels/level'
    i = 1
    while True:
        if not os.path.isfile(name + str(i) + '.txt'):
            name = name + str(i) + '.txt'
            break
        i += 1
    with open(name, 'w', encoding='utf-8') as savefile:
        for sprite in all_sprites:
            if type(sprite) != Button:
                stroka = str(type(sprite).__name__) + ' ' + str(sprite.rect.x) + '-' + str(sprite.rect.y)
                if sprite.type:
                    stroka += ' ' + sprite.type
                stroka += '\n'
                savefile.write(stroka)


running = True
choised = Player
side = False
btn = Button()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] <= 500:
                if event.button == 1:
                    is_player = False
                    for sprite in all_sprites:
                        if type(sprite) == Player:
                            is_player = True
                    if choised == Player:
                        if not is_player:
                            ch = choised(event.pos, side)
                    else:
                        ch = choised(event.pos, side)
                elif event.button == 3:
                    mouse = pygame.sprite.Sprite()
                    mouse.image = pygame.Surface((1, 1))
                    mouse.rect = mouse.image.get_rect()
                    mouse.rect.center = event.pos
                    pygame.sprite.spritecollide(mouse, all_sprites, True)
                    mouse.kill()
            else:
                mouse = pygame.sprite.Sprite()
                mouse.image = pygame.Surface((1, 1))
                mouse.rect = mouse.image.get_rect()
                mouse.rect.center = event.pos
                if pygame.sprite.collide_rect(mouse, btn):
                    save_into_file()
                    running = False
                mouse.kill()
        if event.type == pygame.KEYDOWN:
            if event.key == K_1:
                choised = Player
                side = False
            elif event.key == K_2:
                choised = CommonEnemy
                side = False
            elif event.key == K_3:
                side = 'top'
                choised = ShootingEnemy
            elif event.key == K_4:
                side = 'bottom'
                choised = ShootingEnemy
            elif event.key == K_5:
                side = 'left'
                choised = ShootingEnemy
            elif event.key == K_6:
                side = 'right'
                choised = ShootingEnemy
    img = choised((50, 530), side)
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (255, 0, 0), (0, 500), (width, 500), 2)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    img.kill()
pygame.quit()
