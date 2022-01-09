from decor import *
from player import *
import pygame


pygame.init()
size = WIDTH, HEIGHT = 1060, 560
FPS = 120
LEFT = 30
TOP = 30
CELL_SIZE = 50

screen = pygame.display.set_mode(size)
menu_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = 'data/' + name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def text_render(text, check=0):
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for letter in text:
        string_rendered = font.render(letter, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        if check == 0:
            text_coord += 10
            intro_rect.x = 10
            text_coord += intro_rect.height
            intro_rect.top = text_coord
        else:
            text_coord = 10
            intro_rect.x += 10
            intro_rect.y = 260
        screen.blit(string_rendered, intro_rect)


def death(player, win=False):
    max_count = 40
    death_text = ["Поздравляю, ты помер)", "",
                  f"Заработанные очки: {player.points}",
                  f"Комнат зачищено: {player.rooms}",
                  f'Врагов убито: {player.enemies_killed}',
                  f"Увековечь себя, введи имя, максимум - {max_count} символов"]
    if win:
        death_text[0] = 'Поздравляю, ты выиграл!'
    running = True
    fon = pygame.transform.scale(load_image('menu_image.PNG'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    name = ''
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.unicode == '\x08':
                    name = name[:-1]
                elif len(name) < max_count:
                    if event.key == pygame.K_RETURN:
                        return name
                    else:
                        name += event.unicode
        if running:
            fon = pygame.transform.scale(load_image('menu_image.PNG'), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))
            text_render(death_text)
            text_render(name.split(), 1)
            pygame.display.flip()
            clock.tick(FPS)

