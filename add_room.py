from decor import *
from player import *
from Death import *
import pygame
from constants import *


pygame.init()

screen = pygame.display.set_mode(size)
menu_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()


def your_room():
    max_count = 40
    death_text = ["Что ж, решил ты добавить свою комнату.", "Хорошо, введи название txt (!?) файла.",
                  "Думаешь, ты умнее меня? Думашь, ты лучше меня? Думаешь, можно ввести название не txt файла?",
                  "Да, ты прав, но с последним выйдет фигня, моя предусмотреть такой поворот.",
                  'Эта строчка бесполезна, как и я.',
                  "P.S. Можно не указывать, что это txt файл, я не обижусь."]
    running = True
    fon = pygame.transform.scale(load_image('menu_image.PNG'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    file_name = ''
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.unicode == '\x08':
                    file_name = file_name[:-1]
                elif len(file_name) < max_count:
                    if event.key == pygame.K_RETURN:
                        if file_name.endswith('.txt') is False:
                            file_name += '.txt'
                        return file_name
                    else:
                        file_name += event.unicode
        if running:
            fon = pygame.transform.scale(load_image('menu_image.PNG'), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))
            text_render(death_text)
            text_render(file_name.split(), 1)
            pygame.display.flip()
            clock.tick(FPS)