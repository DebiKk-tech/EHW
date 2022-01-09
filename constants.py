
COLORS = ['floor', 'plant', 'floor', 'floor', 'cupboard', 'floor', 'floor', 'floor', 'table', 'door']
LEFT = 30
TOP = 30
CELL_SIZE = 50
SPACE = 31
SPACE_WITH_DOOR = 128
WIDTH, HEIGHT = 1060, 560
FPS = 120
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 50
POINTS_TIMER = 360
ADD_POINTS_ROOM = 90
ADD_POINTS_ENEMY = 15
LOAD_INTO_BD = 'insert into data(name, score, class, rooms, enemies) VALUES(?, ?, ?, ?, ?)'
BLUE = (0, 0, 255)
BULLET_SPEED = 6
ENEMY_BULLET_SPEED = 4
YELLOW = (255, 255, 0)
ENEMY_SPEED = 2
START_POINTS = 600
EXPLOSION_LIVES = 60
ENEMY_RELOAD = 120
BOSS_SPAWN_RELOAD = 600
BOSS_SHOOT_RELOAD = 60
WARRIOR = {
    'speed': 4,
    'health': 7,
    'reload': 30,
    'bullet_speed': False
}

ARCHER = {
    'speed': 4,
    'health': 5,
    'reload': 25,
    'bullet_speed': 6
}

WIZARD = {
    'speed': 3,
    'health': 4,
    'reload': 100,
    'bullet_speed': 3
}

CHARACTERS = {
    'archer': ARCHER,
    'wizard': WIZARD,
    'warrior': WARRIOR,
}
