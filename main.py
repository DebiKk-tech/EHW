# Талдин М.
import pygame
from decor import *
from player import *
from pygame.constants import K_e


pygame.init()
size = WIDTH, HEIGHT = 1060, 560
FPS = 120
LEFT = 30
TOP = 30
CELL_SIZE = 50

screen = pygame.display.set_mode(size)
menu_sprites = pygame.sprite.Group()
class_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
room_sprites = get_decorate()


def start_game(player_class):
    global cur_ind
    global LEFT, TOP, CELL_SIZE
    print(player_class)
    running = True
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    room_sprites = get_decorate()
    for group in room_sprites:
        for sprite in group:
            all_sprites.add(sprite)
    pl = create_player(WIDTH // 2, HEIGHT // 2, player_group, enemies, bullets, size, player_class, all_sprites)
    if pl.type == 'warrior':
        sword = Sword(player_group, pl, 'top')
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
                        create_enemy(coords[0], coords[1], pl, all_sprites, enemies, bullets, player_group)
        if pygame.key.get_pressed()[K_e] and pl.reload <= 0:
            sword.swinging = -1
            pl.reload = 30
        if not pl.alive():
            running = False
            for sprited in all_sprites:
                all_sprites.remove(sprited)
            create_menu()
            break
        if running:
            screen.fill((0, 0, 0))
            all_sprites.draw(screen)
            all_sprites.update()
            player_group.update()
            player_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)


def select_class():
    running = True
    menu_sprite_background = pygame.sprite.Sprite(class_sprites)
    menu_sprite_background.image = load_image('menu_image.png')
    menu_sprite_background.rect = menu_sprite_background.image.get_rect()
    warrior = pygame.sprite.Sprite(class_sprites)
    warrior.image = pygame.Surface((40, 40))
    warrior.image.fill((255, 0, 0))
    warrior.rect = warrior.image.get_rect()
    warrior.rect.x = 40
    warrior.rect.y = 205
    archer = pygame.sprite.Sprite(class_sprites)
    archer.image = pygame.Surface((40, 40))
    archer.image.fill((0, 255, 0))
    archer.rect = archer.image.get_rect()
    archer.rect.x = 380
    archer.rect.y = 205
    wizard = pygame.sprite.Sprite(class_sprites)
    wizard.image = pygame.Surface((40, 40))
    wizard.image.fill((0, 0, 255))
    wizard.rect = wizard.image.get_rect()
    wizard.rect.x = 720
    wizard.rect.y = 205
    cursor_sprite = pygame.sprite.Sprite(class_sprites)
    cursor_sprite.image = load_image('cursor_image.png')
    cursor_sprite.rect = cursor_sprite.image.get_rect()
    coords = pygame.mouse.get_pos()
    cursor_sprite.rect.center = coords
    class_sprites.draw(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEMOTION:
                coords = pygame.mouse.get_pos()
                cursor_sprite.rect.x, cursor_sprite.rect.y = coords
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.collide_rect(cursor_sprite, warrior):
                    running = False
                    for spritet in class_sprites:
                        spritet.kill()
                    return 'warrior'
                elif pygame.sprite.collide_rect(cursor_sprite, archer):
                    running = False
                    for spritet in class_sprites:
                        spritet.kill()
                    return 'archer'
                elif pygame.sprite.collide_rect(cursor_sprite, wizard):
                    running = False
                    for spritet in class_sprites:
                        spritet.kill()
                    return 'wizard'

                    # start_game()
        if running:
            screen.fill((0, 0, 0))
            class_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)


# Костя К.
def create_menu():
    running = True
    menu_sprite_background = pygame.sprite.Sprite(menu_sprites)
    menu_sprite_background.image = load_image('menu_image.png')
    menu_sprite_background.rect = menu_sprite_background.image.get_rect()
    button_sprite = pygame.sprite.Sprite(menu_sprites)
    button_sprite.image = load_image('main_text.xcf')
    button_sprite.rect = button_sprite.image.get_rect()
    button_sprite.rect.x = 250
    button_sprite.rect.y = 120
    pygame.mouse.set_visible(False)
    cursor_sprite = pygame.sprite.Sprite(menu_sprites)
    cursor_sprite.image = load_image('cursor_image.png')
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
                    start_game(select_class())
        if running:
            screen.fill((0, 0, 0))
            menu_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
create_menu()