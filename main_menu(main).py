# Талдин М.
import pygame
from decor import *
from player import *


pygame.init()
size = WIDTH, HEIGHT = 1060, 560
FPS = 120
LEFT = 30
TOP = 30
CELL_SIZE = 50

screen = pygame.display.set_mode(size)
menu_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
room_sprites = get_decorate()


def start_game():
    global cur_ind
    global LEFT, TOP, CELL_SIZE
    running = True
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    room_sprites = get_decorate()
    for group in room_sprites:
        for sprite in group:
            all_sprites.add(sprite)
    pl = create_player(WIDTH // 2, HEIGHT // 2, player_group, enemies, bullets, size)
    all_sprites.draw(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == NEW_ROOM:
                new = False
                if pl.rect.x - LEFT <= CELL_SIZE:
                    if cur_ind != 0:
                        cur_ind -= 1
                    else:
                        continue
                else:
                    cur_ind += 1
                    new = True
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
                pl.rect.center = WIDTH // 2, HEIGHT // 2
                if new:
                    for coords in [(0, 0), (WIDTH - 70, 0), (0, HEIGHT - 70), (WIDTH, HEIGHT)]:
                        create_enemy(coords[0], coords[1], pl, all_sprites, enemies, bullets)
        if not pl.alive():
            running = False
            for sprited in all_sprites:
                all_sprites.remove(sprited)
            create_menu()
        if running:
            screen.fill((0, 0, 0))
            all_sprites.draw(screen)
            all_sprites.update()
            player_group.update()
            player_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)


# Костя К.
def create_menu():
    running = True
    menu_sprite_background = pygame.sprite.Sprite(menu_sprites)
    menu_sprite_background.image = load_image('menu_image.jpeg')
    menu_sprite_background.rect = menu_sprite_background.image.get_rect()
    button_sprite = pygame.sprite.Sprite(menu_sprites)
    button_sprite.image = load_image('main_text.xcf')
    button_sprite.rect = button_sprite.image.get_rect()
    button_sprite.rect.x = 250
    button_sprite.rect.y = 120
    pygame.mouse.set_visible(False)
    cursor_sprite = pygame.sprite.Sprite(menu_sprites)
    cursor_sprite.image = load_image('cursor_image.jpeg')
    cursor_sprite.rect = cursor_sprite.image.get_rect()
    coords = pygame.mouse.get_pos()
    cursor_sprite.rect.center = coords
    menu_sprites.draw(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEMOTION:
                coords = pygame.mouse.get_pos()
                cursor_sprite.rect.x, cursor_sprite.rect.y = coords
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.collide_rect(cursor_sprite, button_sprite):
                    running = False
                    for spritet in menu_sprites:
                        spritet.kill()
                    start_game()
        if running:
            screen.fill((0, 0, 0))
            menu_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
create_menu()