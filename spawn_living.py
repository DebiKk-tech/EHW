import pygame
from pygame.constants import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_a, K_w, K_s, K_d

PLAYER_SPEED = 4
RELOAD = 30
BULLET_SPEED = 6
YELLOW = pygame.Color('yellow')
BLUE = (0, 0, 255)
ENEMY_SPEED = 2


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
        self.image.fill(BLUE)
        self.rect.centerx = width // 2
        self.rect.centery = height // 2
        self.speedx, self.speedy = 0, 0
        self.reload = RELOAD

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[K_a] and self.rect.left > 0:
            self.speedx = -PLAYER_SPEED
        elif keystate[K_d] and self.rect.right < width:
            self.speedx = PLAYER_SPEED
        if keystate[K_w] and self.rect.top > 0:
            self.speedy = -PLAYER_SPEED
        elif keystate[K_s] and self.rect.bottom < height:
            self.speedy = PLAYER_SPEED
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.reload <= 0:
            if keystate[K_LEFT]:
                create_bullet('left', self)
                self.reload = RELOAD
            elif keystate[K_RIGHT]:
                create_bullet('right', self)
                self.reload = RELOAD
            elif keystate[K_UP]:
                create_bullet('top', self)
                self.reload = RELOAD
            elif keystate[K_DOWN]:
                create_bullet('down', self)
                self.reload = RELOAD
        self.reload -= 1


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
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
        self.image.fill((220, 20, 60))
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx, self.speedy = 0, 0
        self.target = player

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
        if pygame.sprite.spritecollide(self, bullets, True):
            self.kill()


def create_bullet(side, player):
    bul = Bullet(side, player)
    all_sprites.add(bul)
    bullets.add(bul)


def create_enemy(x, y, player):
    en = Enemy(x, y, player)
    all_sprites.add(en)
    enemies.add(en)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1060, 560
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pl = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(pl)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    running = True
    for coords in [(10, 10), (10, height - 10), (width - 10, 10), (width - 10, height - 10)]:
        create_enemy(coords[0], coords[1], pl)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(60)
        if pygame.sprite.spritecollide(pl, enemies, True):
            running = False
    pygame.quit()