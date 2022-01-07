# Талдин М.
import pygame
from pygame.constants import K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_RIGHT, K_LEFT
from decor import *
import os
import sys


def load_image(name, colorkey=None):
    fullname = 'data/' + name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


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
    def __init__(self, x, y, sprites_group, enemy_group, bullet_group, size, type, all_sprites, walls, doors):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.walls = walls
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
        self.doors = doors

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[K_a] and self.rect.left > 31:
            self.speedx = -self.speed
        elif keystate[K_d] and self.rect.right < self.width - 31:
            self.speedx = self.speed
        if keystate[K_w] and self.rect.top > 31:
            self.speedy = -self.speed
        elif keystate[K_s] and self.rect.bottom < self.height - 31:
            self.speedy = self.speed
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if pygame.sprite.spritecollide(self, self.doors, False) and len(self.enemies) == 0:
            ev = pygame.event.Event(NEW_ROOM)
            pygame.event.post(ev)

        if self.reload <= 0 and self.type != 'warrior':
            if keystate[K_LEFT]:
                CHARACTERS[self.type]['attack']('left', self, self.all_sprites, self.bullets, self.walls)
                self.reload = CHARACTERS[self.type]['reload']
            elif keystate[K_RIGHT]:
                CHARACTERS[self.type]['attack']('right', self, self.all_sprites, self.bullets, self.walls)
                self.reload = CHARACTERS[self.type]['reload']
            elif keystate[K_UP]:
                CHARACTERS[self.type]['attack']('top', self, self.all_sprites, self.bullets, self.walls)
                self.reload = CHARACTERS[self.type]['reload']
            elif keystate[K_DOWN]:
                CHARACTERS[self.type]['attack']('down', self, self.all_sprites, self.bullets, self.walls)
                self.reload = CHARACTERS[self.type]['reload']
        self.reload -= 1
        collided_enemies = pygame.sprite.spritecollide(self, self.enemies, True)
        for _ in collided_enemies:
            self.health -= 1
        if self.health == 0:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, side, pl, walls):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.explosive = False
        self.exploded = False
        self.walls = walls
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
        if pygame.sprite.spritecollide(self, self.walls, False):
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
    def __init__(self, x, y, player, bullets_group, player_group):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
        self.image.fill((220, 20, 60))
        self.rect.x = x
        self.rect.y = y
        self.speedx, self.speedy = 0, 0
        self.target = player
        self.bullet_group = bullets_group
        self.player_group = player_group

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
        collide_list2 = pygame.sprite.spritecollide(self, self.player_group, False)
        collide_list += collide_list2
        for collided in collide_list:
            if type(collided) == Sword and collided.swinging != -2 or type(collided) == Bullet:
                self.kill()
                if len(self.target.enemies) == 0:
                    for door in self.target.doors:
                        door.set_opened()


class Sword(pygame.sprite.Sprite):
    def __init__(self, group, player, side):
        super().__init__(group)
        self.image = pygame.transform.flip(load_image('sword_on.xcf'), True, False)
        self.rect = self.image.get_rect()
        self.rect.bottom, self.rect.right = player.rect.top + 5, player.rect.left + 5
        self.player = player
        self.swinging = -2
        self.start_image = self.image
        self.swinged = False
        self.countdown = 1
        self.side = side
        self.main_image = self.image

    def update(self):
        keystate = pygame.key.get_pressed()
        self.main_image = load_image('sword_on.xcf')
        if keystate[K_UP] and not self.side == 'top' and self.swinging == -2:
            self.player.reload = 30
            self.side = 'top'
            if self.swinged:
                rotate(self, pygame.transform.flip(self.main_image, False, False), 0)
            else:
                rotate(self, pygame.transform.flip(self.main_image, True, False), 0)
        elif keystate[K_DOWN] and not self.side == 'bottom' and self.swinging == -2:
            self.player.reload = 30
            self.side = 'bottom'
            if self.swinged:
                rotate(self, pygame.transform.flip(self.main_image, False, False), 0)
            else:
                rotate(self, pygame.transform.flip(self.main_image, True, False), 0)
        elif keystate[K_LEFT] and not self.side == 'left' and self.swinging == -2:
            self.player.reload = 30
            self.side = 'left'
            if self.swinged:
                rotate(self, self.main_image, -90)
            else:
                rotate(self, pygame.transform.flip(self.main_image, True, False), -90)
        elif keystate[K_RIGHT] and not self.side == 'right' and self.swinging == -2:
            self.player.reload = 30
            self.side = 'right'
            if self.swinged:
                rotate(self, self.main_image, -90)
            else:
                rotate(self, pygame.transform.flip(self.main_image, True, False), -90)
        if self.swinging == -2:
            self.start_image = self.image
        if self.side == 'top':
            if self.swinging == 1:
                self.rect.bottom, self.rect.left = self.player.rect.top + 5, self.player.rect.centerx
            if (self.swinged and not self.swinging == 2) or (self.swinging == 2 and not self.swinged):
                self.rect.bottom, self.rect.left = self.player.rect.top + 5, self.player.rect.right - 20
            else:
                self.rect.bottom, self.rect.right = self.player.rect.top + 5, self.player.rect.left + 20
        elif self.side == 'bottom':
            if self.swinging == 1:
                self.rect.top, self.rect.left = self.player.rect.bottom - 5, self.player.rect.centerx
            if (self.swinged and not self.swinging == 2) or (self.swinging == 2 and not self.swinged):
                self.rect.top, self.rect.left = self.player.rect.bottom - 5, self.player.rect.right - 20
            else:
                self.rect.top, self.rect.right = self.player.rect.bottom - 5, self.player.rect.left + 20
        elif self.side == 'left':
            if self.swinging == 1:
                self.rect.top, self.rect.left = self.player.rect.centery, self.player.rect.left + 5
            if (self.swinged and not self.swinging == 2) or (self.swinging == 2 and not self.swinged):
                self.rect.top, self.rect.right = self.player.rect.bottom - 20, self.player.rect.left + 5
            else:
                self.rect.bottom, self.rect.right = self.player.rect.top + 20, self.player.rect.left + 5
        elif self.side == 'right':
            if self.swinging == 1:
                self.rect.top, self.rect.right = self.player.rect.centery, self.player.rect.right - 5
            if (self.swinged and not self.swinging == 2) or (self.swinging == 2 and not self.swinged):
                self.rect.top, self.rect.left = self.player.rect.bottom - 20, self.player.rect.right - 5
            else:
                self.rect.bottom, self.rect.left = self.player.rect.top + 20, self.player.rect.right - 5
        if self.swinging != -2 and not self.countdown:
            self.swinging += 1
            angle = -45
            if self.swinged:
                angle = 45
            if self.side in ['left', 'bottom']:
                angle = -angle
            rotate(self, self.start_image, (self.swinging + 1) * angle)
            self.countdown = 1
        elif self.countdown:
            self.countdown -= 1
        if self.swinging == 3:
            self.swinging = -2
            self.swinged = not self.swinged
            self.main_image = pygame.transform.flip(self.image, False, True)
            if self.side in ['top', 'bottom']:
                self.image = pygame.transform.flip(self.image, False, True)
            else:
                self.image = pygame.transform.flip(self.image, True, False)
            self.start_image = self.image


def rotate(target, image, angle):
    coords = target.rect.center
    target.image = pygame.transform.rotate(image, angle)
    target.rect = target.image.get_rect()
    target.rect.center = coords


def create_player(x, y, sprites_group, enemy_group, bullet_group, size, player_type, all_sprites, walls, doors):
    pl = Player(x, y, sprites_group, enemy_group, bullet_group, size, player_type, all_sprites, walls, doors)
    sprites_group.add(pl)
    return pl


def create_bullet(side, player, sprites_group, bullets_group, walls):
    bul = Bullet(side, player, walls)
    sprites_group.add(bul)
    bullets_group.add(bul)


def create_enemy(x, y, player, sprites_group, enemy_group, bullets_group, player_group):
    en = Enemy(x, y, player, bullets_group, player_group)
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
