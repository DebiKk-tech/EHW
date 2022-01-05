import pygame

from player import *
from decor import *


def init(check, pl=None, board=None, cur_ind=None, enemies=None):
    pass


pygame.init()
size = WIDTH, HEIGHT = 1060, 560
FPS = 120
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
clock = pygame.time.Clock()
room_sprites = get_decorate()
for group in room_sprites:
    for sprite in group:
        all_sprites.add(sprite)
running = True
pl = create_player(WIDTH // 2, HEIGHT // 2, all_sprites, enemies, bullets, size)
for coords in [(0, 0), (WIDTH - 70, 0), (0, HEIGHT - 70), (WIDTH, HEIGHT)]:
    create_enemy(coords[0], coords[1], pl, all_sprites, enemies, bullets)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or not pl.alive():
            running = False
        if event.type == NEW_ROOM:
            if pl.rect.x - LEFT <= CELL_SIZE:
                if cur_ind != 0:
                    cur_ind -= 1
                else:
                    continue
            else:
                cur_ind += 1
            if cur_ind >= len(boards):
                board = Board(20, 10)
                boards.append(board)
            cur_board = boards[cur_ind]
            for sprite in all_sprites:
                sprite.kill()
            cur_board.render()
            room_sprites = get_decorate()
            for group in room_sprites:
                for sprite in group:
                    all_sprites.add(sprite)
            pl = create_player(WIDTH // 2, HEIGHT // 2, all_sprites, enemies, bullets, size)
            for coords in [(0, 0), (WIDTH - 70, 0), (0, HEIGHT - 70), (WIDTH, HEIGHT)]:
                create_enemy(coords[0], coords[1], pl, all_sprites, enemies, bullets)
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
