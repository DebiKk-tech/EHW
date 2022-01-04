# Талдин М.
import pygame
from spawn_living import *
from decor import *
from walls import Wall

pygame.init()
size = WIDTH, HEIGHT = 1060, 560
FPS = 60
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
walls = pygame.sprite.Group()

room_sprites = get_decorate()
for group in room_sprites:
    for sprite in group:
        all_sprites.add(sprite)

clock = pygame.time.Clock()
running = True
pl = create_player(WIDTH // 2, HEIGHT // 2, all_sprites, enemies, bullets, size)

wall1 = Wall(0, 0, 1060, 31, [all_sprites, walls])
wall2 = Wall(0, 0, 31, 560, [all_sprites, walls])
wall3 = Wall(1030, 0, 31, 560, [all_sprites, walls])
wall4 = Wall(0, 530, 1060, 31, [all_sprites, walls])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or not pl.alive():
            running = False

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()