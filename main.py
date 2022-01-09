# Талдин М.
from constants import *
import pygame
from decor import *
from player import *
from pygame.constants import K_SPACE
from walls import *
from Death import death
from random import randint
from add_room import *
import os


pygame.init()
size = WIDTH, HEIGHT + 50  # Добавляется 50-пиксельное пространство для интерфейса, которое остальная игра не учитывает

screen = pygame.display.set_mode(size)
size = WIDTH, HEIGHT
menu_sprites = pygame.sprite.Group()
class_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
room_sprites = get_decorate()


def render_text(x, y, text, surface):
    font = pygame.font.Font(None, FONT_SIZE)
    text = font.render(text, True, WHITE)
    text_x = x
    text_y = y
    surface.blit(text, (text_x, text_y))


def start_game(player_class, loading_level=False):
    global cur_ind, boards
    global LEFT, TOP, CELL_SIZE
    running = True
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enemies_bullets = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    doors = pygame.sprite.Group()
    wall1 = Wall(0, 0, [walls, player_group], 'horizontalzerodayn.xcf')
    wall2 = Wall(0, 0, [walls, player_group], 'verticalwall.xcf')
    wall3 = Wall(1030, 0, [walls, player_group], 'verticalwall.xcf')
    wall4 = Wall(0, 530, [walls, player_group], 'horizontalzerodayn.xcf')
    door1 = Door(size, 'left', [doors])
    door1.set_closed()
    door2 = Door(size, 'right', [doors])
    DECREASE_POINTS_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(DECREASE_POINTS_EVENT, POINTS_TIMER)
    room_sprites = get_decorate()
    for group in room_sprites:
        for sprite in group:
            all_sprites.add(sprite)
    pl = create_player(WIDTH // 2, HEIGHT // 2, player_group, enemies, bullets, size, player_class, all_sprites, walls,
                       doors, create_menu)
    if pl.type == 'warrior':
        sword = Sword(player_group, pl, 'top')
    if loading_level:
        load_from_file(loading_level, pl, all_sprites, enemies, bullets, player_group,
                       enemies_bullets)
    all_sprites.draw(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == DECREASE_POINTS_EVENT and pl.points >= 3:
                pl.points -= 3
            if event.type == NEW_ROOM:
                new = False
                if pl.rect.x - LEFT <= CELL_SIZE * 3:
                    if cur_ind != 0:
                        cur_ind -= 1
                        if cur_ind == 0:
                            door1.set_closed()
                        else:
                            door1.set_opened()
                            door2.set_opened()
                        pl.rect.center = WIDTH - SPACE_WITH_DOOR, HEIGHT // 2
                    else:
                        continue
                else:
                    cur_ind += 1
                    pl.rect.center = SPACE_WITH_DOOR, HEIGHT // 2
                    door1.set_opened()
                if cur_ind >= len(boards):
                    door1.set_closed()
                    board = Board(20, 10)
                    boards.append(board)
                    new = True
                    pl.rooms += 1
                    pl.points += ADD_POINTS_ROOM
                    for door in doors:
                        door.set_closed()
                cur_board = boards[cur_ind]
                for sprite in all_sprites:
                    sprite.kill()
                cur_board.render()
                room_sprites = get_decorate()
                for group in room_sprites:
                    for sprite in group:
                        all_sprites.add(sprite)
                if new:
                    if cur_ind == 9 and not loading_level:
                        create_enemy(0, 0, pl, all_sprites, enemies, bullets, player_group, 'boss', enemies_bullets)
                    else:
                        load_from_file('level' + str(randint(1, 5)) + '.txt', pl, all_sprites, enemies, bullets,
                                       player_group, enemies_bullets)
        if pygame.key.get_pressed()[K_SPACE] and pl.reload <= 0 and pl.type == 'warrior':
            sword.swinging = -1
            pl.reload = 30
        if not pl.alive():
            running = False
            for sprited in all_sprites:
                all_sprites.remove(sprited)
            if not loading_level:
                death(pl)
            create_menu(True)
            break
        if len(enemies) == 0 and cur_ind != 0:
            door1.set_opened()
            door2.set_opened()
        if len(enemies) != 0:
            door1.set_closed()
            door2.set_closed()
        if running:
            screen.fill(BLACK)
            doors.draw(screen)
            doors.update()
            all_sprites.draw(screen)
            all_sprites.update()
            player_group.update()
            player_group.draw(screen)
            render_text(20, 570, 'Ваше здоровье: ' + str(pl.health), screen)
            render_text(500, 570, 'Ваши очки: ' + str(pl.points), screen)
            pygame.display.flip()
            clock.tick(FPS)
            print(cur_ind)


def load_from_file(filename, pl, all_sprites, enemies, bullets, player_group, enemies_bullets):
    if os.path.isfile('levels/' + filename):
        with open('levels/' + filename, 'r', encoding='utf-8') as savefile:
            lines = savefile.readlines()
            for j in range(len(lines)):
                if lines[j] != '':
                    lines[j] = lines[j].split()
                    lines[j][1] = lines[j][1].split('-')
                    lines[j][1][0], lines[j][1][1] = int(lines[j][1][0]), int(lines[j][1][1])
                    lines[j][1] = tuple(lines[j][1])
            for line in lines:
                if line[0] == 'CommonEnemy':
                    create_enemy(line[1][0] - 20, line[1][1] - 20, pl, all_sprites, enemies, bullets, player_group,
                                 'common')
                if line[0] == 'ShootingEnemy':
                    create_enemy(line[1][0] - 20, line[1][1] - 20, pl, all_sprites, enemies, bullets, player_group,
                                 'shooting-' + line[2], enemies_bullets)
                if line[0] == 'Player':
                    pl.rect.center = line[1][0] - 20, line[1][1] - 20


# Александр Ч.


def select_class():
    running = True
    menu_sprite_background = pygame.sprite.Sprite(class_sprites)
    menu_sprite_background.image = load_image('menu_image.png')
    menu_sprite_background.rect = menu_sprite_background.image.get_rect()
    warrior = pygame.sprite.Sprite(class_sprites)
    warrior.image = load_image('swordsman.xcf')
    warrior.rect = warrior.image.get_rect()
    warrior.rect.x = 40
    warrior.rect.y = 205
    archer = pygame.sprite.Sprite(class_sprites)
    archer.image = load_image('bowman.xcf')
    archer.rect = archer.image.get_rect()
    archer.rect.x = 380
    archer.rect.y = 205
    wizard = pygame.sprite.Sprite(class_sprites)
    wizard.image = load_image('drugman.xcf')
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
                sys.exit()
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
        if running:
            screen.fill((0, 0, 0))
            class_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)


# Костя К.
def create_menu(new_game=False):
    global cur_ind, boards
    cur_ind = 0
    if new_game:
        boards = [boards[0]]
    running = True
    menu_sprite_background = pygame.sprite.Sprite(menu_sprites)
    menu_sprite_background.image = load_image('menu_image.png')
    menu_sprite_background.rect = menu_sprite_background.image.get_rect()
    button_sprite = pygame.sprite.Sprite(menu_sprites)
    button_sprite.image = load_image('main_text.xcf')
    button_sprite.rect = button_sprite.image.get_rect()
    button_sprite.rect.x = 250
    button_sprite.rect.y = 120
    add_loc_btn = pygame.sprite.Sprite(menu_sprites)
    add_loc_btn.image = load_image('add_room_btn.png')
    add_loc_btn.rect = add_loc_btn.image.get_rect()
    add_loc_btn.rect.x = 250
    add_loc_btn.rect.y = 320
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
                if pygame.sprite.collide_rect(cursor_sprite, add_loc_btn):
                    running = False
                    for spritet in menu_sprites:
                        spritet.kill()
                    level = your_room()
                    start_game(select_class(), level)
        if running:
            screen.fill((0, 0, 0))
            menu_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
create_menu()