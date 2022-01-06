# Талдин М.
import pygame
from pygame.constants import K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_RIGHT, K_LEFT
from decor import *

BULLET_SPEED = 6
YELLOW = pygame.Color('yellow')
BLUE = (0, 0, 255)
ENEMY_SPEED = 2
NEW_ROOM = pygame.USEREVENT + 1
FPS = 120
LEFT = 30
TOP = 30
CELL_SIZE = 50


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites_group, enemy_group, bullet_group, size, type, all_sprites):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
        self.image.fill(BLUE)
        self.rect.centerx = x
        self.rect.centery = y
        self.type = type
        self.speedx, self.speedy = 0, 0
        self.reload = CHARACTERS[self.type]['reload']
        self.health = CHARACTERS[self.type]['health']
        self.speed = CHARACTERS[self.type]['speed']
        self.enemies = enemy_group
        self.width, self.height = size
        self.sprites, self.bullets = sprites_group, bullet_group
        self.all_sprites = all_sprites

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[K_a] and self.rect.left > 0:
            self.speedx = -self.speed
        elif keystate[K_d] and self.rect.right < self.width:
            self.speedx = self.speed
        if keystate[K_w] and self.rect.top > 0:
            self.speedy = -self.speed
        elif keystate[K_s] and self.rect.bottom < self.height:
            self.speedy = self.speed
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if (self.rect.x > self.width - 2 * LEFT - CELL_SIZE // 2 or self.rect.x < LEFT) and (self.height - 2 * TOP) // 2 - CELL_SIZE < \
                self.rect.y < (self.height - 2 * TOP) // 2 + CELL_SIZE and len(self.enemies) == 0:
            ev = pygame.event.Event(NEW_ROOM)
            pygame.event.post(ev)

        if self.reload <= 0:
            if keystate[K_LEFT]:
                CHARACTERS[self.type]['attack']('left', self, self.all_sprites, self.bullets)
                self.reload = CHARACTERS[self.type]['reload']
            elif keystate[K_RIGHT]:
                CHARACTERS[self.type]['attack']('right', self, self.all_sprites, self.bullets)
                self.reload = CHARACTERS[self.type]['reload']
            elif keystate[K_UP]:
                CHARACTERS[self.type]['attack']('top', self, self.all_sprites, self.bullets)
                self.reload = CHARACTERS[self.type]['reload']
            elif keystate[K_DOWN]:
                CHARACTERS[self.type]['attack']('down', self, self.all_sprites, self.bullets)
                self.reload = CHARACTERS[self.type]['reload']
        self.reload -= 1
        if pygame.sprite.spritecollide(self, self.enemies, True):
            self.health -= 1
        if self.health == 0:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, side, pl):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.explosive = False
        self.exploded = False
        if pl.type == 'wizard':
            self.explosive = True
        if side == 'left' or side == 'right':
            self.rect.centery = pl.rect.centery
            if side == 'left':
                self.rect.left = pl.rect.left
                self.speedx = pl.speedx // 2 - CHARACTERS[pl.type]['bullet_speed']
            else:
                self.rect.right = pl.rect.right
                self.speedx = pl.speedx // 2 + CHARACTERS[pl.type]['bullet_speed']
            self.speedy = pl.speedy // 2
        else:
            self.rect.centerx = pl.rect.centerx
            if side == 'top':
                self.rect.top = pl.rect.top
                self.speedy = pl.speedy // 2 - CHARACTERS[pl.type]['bullet_speed']
            else:
                self.rect.bottom = pl.rect.bottom
                self.speedy = pl.speedy // 2 + CHARACTERS[pl.type]['bullet_speed']
            self.speedx = pl.speedx // 2
        self.countdown = 60

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.exploded:
            self.countdown -= 1
        if not self.countdown:
            self.kill()

    def explode(self):
        self.exploded = True
        self.speedx, self.speedy = 0, 0
        coords = self.rect.center
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.rect.center = coords


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
        collide_list = pygame.sprite.spritecollide(self, self.bullet_group, False)
        if collide_list:
            for collided in collide_list:
                if collided.explosive:
                    collided.explode()
                else:
                    collided.kill()
            self.kill()


def create_player(x, y, sprites_group, enemy_group, bullet_group, size, player_type, all_sprites):
    pl = Player(x, y, sprites_group, enemy_group, bullet_group, size, player_type, all_sprites)
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


WARRIOR = {
    'speed': 4,
    'health': 4,
    'reload': 30,
    'bullet_speed': False,
    'attack': create_bullet
}

ARCHER = {
    'speed': 4,
    'health': 5,
    'reload': 25,
    'bullet_speed': 6,
    'attack': create_bullet
}

WIZARD = {
    'speed': 2,
    'health': 7,
    'reload': 100,
    'bullet_speed': 3,
    'attack': create_bullet
}

CHARACTERS = {
    'archer': ARCHER,
    'wizard': WIZARD,
    'warrior': WARRIOR,
}
