# Талдин М.
import pygame
from spawn_living import *
from decor import *


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
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()