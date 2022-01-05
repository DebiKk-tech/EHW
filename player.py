# Талдин М.
import pygame
from pygame.constants import K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_RIGHT, K_LEFT
from decor import *

WIDTH, HEIGHT = 1060, 560
PLAYER_SPEED = 4
RELOAD = 30
BULLET_SPEED = 6
YELLOW = pygame.Color('yellow')
BLUE = (0, 0, 255)
ENEMY_SPEED = 2
NEW_ROOM = pygame.USEREVENT + 1


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites_group, enemy_group, bullet_group, size):
        super().__init__(sprites_group)
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
        self.image.fill(BLUE)
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx, self.speedy = 0, 0
        self.reload = RELOAD
        self.enemies = enemy_group
        self.width, self.height = size
        self.sprites, self.bullets = sprites_group, bullet_group

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[K_a] and self.rect.left > 0:
            self.speedx = -PLAYER_SPEED
        elif keystate[K_d] and self.rect.right < self.width:
            self.speedx = PLAYER_SPEED
        if keystate[K_w] and self.rect.top > 0:
            self.speedy = -PLAYER_SPEED
        elif keystate[K_s] and self.rect.bottom < self.height:
            self.speedy = PLAYER_SPEED
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.x > WIDTH - 2 * LEFT - CELL_SIZE // 2 or self.rect.x < LEFT) and (HEIGHT - 2 * TOP) // 2 - CELL_SIZE < \
                self.rect.y < (HEIGHT - 2 * TOP) // 2 + CELL_SIZE:
            ev = pygame.event.Event(NEW_ROOM)
            pygame.event.post(ev)
        if self.reload <= 0:
            if keystate[K_LEFT]:
                create_bullet('left', self, self.sprites, self.bullets)
                self.reload = RELOAD
            elif keystate[K_RIGHT]:
                create_bullet('right', self, self.sprites, self.bullets)
                self.reload = RELOAD
            elif keystate[K_UP]:
                create_bullet('top', self, self.sprites, self.bullets)
                self.reload = RELOAD
            elif keystate[K_DOWN]:
                create_bullet('down', self, self.sprites, self.bullets)
                self.reload = RELOAD
        self.reload -= 1
        if pygame.sprite.spritecollide(self, self.enemies, True):
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, side, pl):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        if side == 'left' or side == 'right':
            self.rect.centery = pl.rect.centery
            if side == 'left':
                self.rect.left = pl.rect.left
                self.speedx = pl.speedx // 2 - BULLET_SPEED
            else:
                self.rect.right = pl.rect.right
                self.speedx = pl.speedx // 2 + BULLET_SPEED
            self.speedy = pl.speedy // 2
        else:
            self.rect.centerx = pl.rect.centerx
            if side == 'top':
                self.rect.top = pl.rect.top
                self.speedy = pl.speedy // 2 - BULLET_SPEED
            else:
                self.rect.bottom = pl.rect.bottom
                self.speedy = pl.speedy // 2 + BULLET_SPEED
            self.speedx = pl.speedx // 2

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player, bullets_group):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
        self.image.fill((220, 20, 60))
        self.rect.x = x
        self.rect.y = y
        self.speedx, self.speedy = 0, 0
        self.target = player
        self.bullet_group = bullets_group

    def update(self):
        if self.rect.centerx > self.target.rect.centerx:
            self.speedx = -ENEMY_SPEED
        else:
            self.speedx = ENEMY_SPEED
        if self.rect.centery > self.target.rect.centery:
            self.speedy = -ENEMY_SPEED
        else:
            self.speedy = ENEMY_SPEED
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.speedy, self.speedx = 0, 0
        # Проверка столкновений
        if pygame.sprite.spritecollide(self, self.bullet_group, True):
            self.kill()


def create_player(x, y, sprites_group, enemy_group, bullet_group, size):
    pl = Player(x, y, sprites_group, enemy_group, bullet_group, size)
    sprites_group.add(pl)
    return pl


def create_bullet(side, player, sprites_group, bullets_group):
    bul = Bullet(side, player)
    sprites_group.add(bul)
    bullets_group.add(bul)


def create_enemy(x, y, player, sprites_group, enemy_group, bullets_group):
    en = Enemy(x, y, player, bullets_group)
    sprites_group.add(en)
    enemy_group.add(en)
