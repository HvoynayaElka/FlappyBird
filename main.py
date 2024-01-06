import pygame
import sys
import os


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(): #пока что такой же как в уроке, потом нуэно будет менять
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_level(filename=None):
    filename = 'map.txt'
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite): #создаёт все спрайты, кроме игрока
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        if tile_type == 'tree':
            environment_sprites.add(self)
            self.rect = self.image.get_rect().move(TILE_WIDHT * pos_x, TILE_HEIGHT * pos_y)
        else:
            obstacles_sprites.add(self)
            self.rect = self.image.get_rect().move(TILE_WIDHT * pos_x, TILE_HEIGHT * pos_y - 10)


class Player(pygame.sprite.Sprite): #создаёт спрайт игрока
    def __init__(self, pos_x, pos_y):
        super().__init__(player_sprite, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(TILE_WIDHT * pos_x + 15, TILE_HEIGHT * pos_y + 5)
        self.mask = pygame.mask.from_surface(self.image)


def generate_level(level): # генерация уровня из файла
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == '*':
                Tile('ground', x, y)
            elif level[y][x] == '!':
                Tile('tree', x, y)
            elif level[y][x] == '-':
                Tile('land', x, y)

    return new_player, x, y


class Camera:
    def __init__(self):
        self.dx = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        if obj.rect.x <= -TILE_WIDHT:
            obj.rect.x += level_x * TILE_WIDHT

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)


pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))

player = None
camera = Camera()


obstacles_sprites = pygame.sprite.Group()
environment_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


TILE_WIDHT = TILE_HEIGHT = 100 #размер одной клетки

tile_images = { #картинки спрайтов
    'wall': pygame.transform.scale(load_image('box.png'), (TILE_WIDHT, TILE_HEIGHT)),
    'ground': pygame.transform.scale(load_image('ground.png', -1), (TILE_WIDHT, TILE_HEIGHT)),
    'tree': pygame.transform.scale(load_image('tree.png'), (TILE_WIDHT, TILE_HEIGHT)),
    'land': pygame.transform.scale(load_image('land.png'), (TILE_WIDHT, TILE_HEIGHT))
}
player_image = load_image('mar.png') #картинка игрока
player_image = pygame.transform.scale(player_image, (TILE_WIDHT * 2, TILE_HEIGHT))

start_screen()
timer = pygame.USEREVENT + 1 #таймер
pygame.time.set_timer(timer, 10)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            terminate()
        if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not player:
            player, level_x, level_y = generate_level(load_level())
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            player.rect = player.rect.move(0, -50)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            player.rect = player.rect.move(0, 50)
        if event.type == timer and player:
            player.rect = player.rect.move(5, 0)
    if player:
        screen.fill((168, 216, 255))
        camera.update(player)
        for sprite in all_sprites:
            if pygame.sprite.collide_mask(player, sprite) and sprite in obstacles_sprites:
                terminate()
            camera.apply(sprite)
    all_sprites.draw(screen)
    player_sprite.draw(screen)
    pygame.display.flip()
