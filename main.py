import pygame
import sys
from Funcs import load_image, load_level


def terminate():
    pygame.quit()
    sys.exit()


class Start_screen:
    def __init__(self):
        screen.blit(fon, (0, 0))
        main_font = pygame.font.Font(None, 150)
        string_rendered = main_font.render('Flappy bird', 1, (168, 168, 168))
        screen.blit(string_rendered, (300, 150))
        texts = ['Играть', 'Выйти']
        text_coord = 300
        delta_coord = 100
        self.player = player
        self.lvl_x = level_x
        self.lvl_y = level_y
        Button(300, text_coord + delta_coord, 300, 50, texts[0], self.start_game)
        Button(300, text_coord + delta_coord * 2, 300, 50, texts[1], self.start_game)

    def start_game(self):
        self.player, self.lvl_x, self.lvl_y = generate_level(load_level())
        Ground(0)
        Ground(1)



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
        if obj in ground_sprites and obj.rect.x <= -WIDTH:
            obj.rect.x += WIDTH * 2
        elif obj in obstacles_sprites and obj.rect.x <= -TILE_WIDHT:
            obj.rect.x += level_x * TILE_WIDHT

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)


class Ground(pygame.sprite.Sprite):
    def __init__(self, k):
        super().__init__(all_sprites, ground_sprites)
        self.image = ground_image
        self.rect = self.image.get_rect().move(WIDTH * k, HEIGHT - TILE_HEIGHT * KOEF)


class Button:
    def __init__(self, x, y, width, height, button_text='Button', onclickFunction=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.button_text = button_text
        self.fillColors = {'normal': (20, 20, 20), 'hover': (255, 128, 128)}
        buttons_list.append(self)
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.main_font = pygame.font.Font(None, 50)
        self.display_text = self.main_font.render(button_text, True, (20, 20, 20))

    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        self.display_text = self.main_font.render(self.button_text, True, self.fillColors["normal"])
        if self.buttonRect.collidepoint(mouse_pos):
            self.display_text = self.main_font.render(self.button_text, True, self.fillColors["hover"])
            if pygame.mouse.get_pressed()[0]:
                self.onclickFunction()
        screen.blit(self.display_text, self.buttonRect)



pygame.init()
WIDTH, HEIGHT = 1920, 1080
KOEF = 1.3
screen = pygame.display.set_mode((WIDTH, HEIGHT))

player = None
level_x = None
level_y = None
camera = Camera()

buttons_list = []
obstacles_sprites = pygame.sprite.Group()
environment_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
ground_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


TILE_WIDHT = TILE_HEIGHT = 100 #размер одной клетки

tile_images = { #картинки спрайтов
    'wall': pygame.transform.scale(load_image('box.png'), (TILE_WIDHT, TILE_HEIGHT)),
    'tree': pygame.transform.scale(load_image('tree.png'), (TILE_WIDHT, TILE_HEIGHT)),
    'land': pygame.transform.scale(load_image('land.png'), (TILE_WIDHT, TILE_HEIGHT))
}
#картинка игрока
player_image = pygame.transform.scale(load_image('mar.png'), (TILE_WIDHT * 2, TILE_HEIGHT))
ground_image = pygame.transform.scale(load_image('ground.png'), (WIDTH, TILE_HEIGHT * KOEF))
background_image = pygame.transform.scale(load_image('background.png'), (WIDTH, HEIGHT))
fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))

Start_screen()
timer = pygame.USEREVENT + 1 #таймер
pygame.time.set_timer(timer, 10)
T = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            terminate()
#        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
#            player.rect = player.rect.move(0, -50)
#        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
#            player.rect = player.rect.move(0, 50)
        if event.type == timer and player:
            player.rect = player.rect.move(5, 0)
    if player:
        screen.fill((0, 0, 0))
        screen.blit(background_image, (T, 0))
        screen.blit(background_image, (T + WIDTH, 0))
        if T < -WIDTH:
            T = 0
        T -= 1
        camera.update(player)
        for sprite in all_sprites:
            if pygame.sprite.collide_mask(player, sprite) and sprite in obstacles_sprites:
                pass
            camera.apply(sprite)
    else:
        for btn in buttons_list:
            btn.process()
    all_sprites.draw(screen)
    player_sprite.draw(screen)
    pygame.display.flip()
