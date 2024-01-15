import pygame
import sys
from Funcs import load_image, load_level


class Start_screen:
    def __init__(self):
        screen.blit(fon, (0, 0))
        main_font = pygame.font.Font(None, 150)
        string_rendered = main_font.render('Flappy bird', 1, "#dd9475")
        screen.blit(string_rendered, (WIDTH / 5, HEIGHT / 6))
        texts = ['Играть', 'Выйти']
        delta_coord = 100
        koef_coord = 0.5
        Button(WIDTH / 20, HEIGHT * koef_coord, 300, 50, menu_buttons, texts[0], start_game)
        Button(WIDTH / 20, HEIGHT * koef_coord + delta_coord, 300, 50, menu_buttons, texts[1], terminate)


class Lose_screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x0 = (WIDTH - self.width) / 2
        self.y0 = (HEIGHT - self.height) / 2
        self.func = None
        self.check = True
        self.Surf = pygame.Surface((self.width, self.height))
        main_font = pygame.font.Font(None, 75)
        self.string_rendered = main_font.render('You lose', 1, "red")
        self.button_list = []
        self.Retry_btn = Button((WIDTH - self.width) * 1.2, (HEIGHT - self.height) * 1.1, retry_btn_image.get_width(),
                                retry_btn_image.get_height(), self.button_list,
                                onclickFunction=self.restart_game, image=retry_btn_image)
        self.Quit_btn = Button((WIDTH - self.width) * 0.6, (HEIGHT - self.height) * 1.1,
                                quit_btn_image.get_width(), quit_btn_image.get_width(), self.button_list,
                                onclickFunction=terminate, image=quit_btn_image)
        self.update()

    def restart_game(self):
        global player, level_x, level_y, is_alive, obstacles_sprites,\
            environment_sprites, player_sprite, ground_sprites, all_sprites, player_cur_score, current_score_text
        obstacles_sprites = pygame.sprite.Group()
        environment_sprites = pygame.sprite.Group()
        player_sprite = pygame.sprite.Group()
        ground_sprites = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        player, level_x, level_y, is_alive = None, None, None, True
        self.check = False
        player_cur_score = 0
        current_score_text = score_font.render(f'Score: {player_cur_score}', 1, "black")
        start_game()

    def update(self):
        self.Surf.blit(self.string_rendered,
                       ((self.Surf.get_width() - self.string_rendered.get_width()) / 2,
                        (self.Surf.get_height() - self.string_rendered.get_height()) / 4))
        while self.check:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    terminate()
            screen.blit(self.Surf, ((WIDTH - self.width) / 2, (HEIGHT - self.height) / 2))
            for btn in self.button_list:
                btn.process()
            pygame.display.flip()


class Tile(pygame.sprite.Sprite):
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
    def __init__(self, k=0, upper=False):
        super().__init__(all_sprites, ground_sprites)
        self.image = ground_image
        if not upper:
            self.rect = self.image.get_rect().move(WIDTH * k, HEIGHT - TILE_HEIGHT * KOEF)
        else:
            self.rect = self.image.get_rect().move(WIDTH * k, -TILE_HEIGHT * KOEF)


class Button:
    def __init__(self, x, y, width, height, btn_group, button_text='Button', onclickFunction=None, image=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.btn_image = image
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.btn_image is None:
            self.button_text = button_text
            self.fillColors = {'normal': (20, 20, 20), 'hover': (255, 128, 128)}
            self.main_font = pygame.font.Font(None, 50)
            self.display_text = self.main_font.render(button_text, True, (20, 20, 20))
        else:
            self.btn_image = image
        btn_group.append(self)

    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.btn_image is None:
            self.display_text = self.main_font.render(self.button_text, True, self.fillColors["normal"])
            if self.buttonRect.collidepoint(mouse_pos):
                self.display_text = self.main_font.render(self.button_text, True, self.fillColors["hover"])
                if pygame.mouse.get_pressed()[0]:
                    self.onclickFunction()
            screen.blit(self.display_text, self.buttonRect)
        else:
            if self.buttonRect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                self.onclickFunction()
            screen.blit(self.btn_image, self.buttonRect)


def start_game():
    global player, level_x, level_y, menu_buttons, score_text
    menu_buttons = []
    player, level_x, level_y = generate_level(load_level('levels\\main_map.txt'))
    Ground(0)
    Ground(1)
    Ground(upper=True)


def generate_level(level): # генерация уровня из файла
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == '!':
                Tile('tree', x, y)
            elif level[y][x] == '-':
                Tile('land', x, y)

    return new_player, x, y


def terminate():
    pygame.quit()
    with open('data\\player result\\info.txt', 'w') as file:
        file.write(str(player_high_score))
    sys.exit()


pygame.init()
WIDTH, HEIGHT = 960, 540
KOEF = 1.4
LOSESCREEN_WIDHT, LOSESCREEN_HEIGHT = WIDTH / 2, HEIGHT / 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))

player = None
player_cur_score = 0
with open('data\\player result\\info.txt') as file:
    player_high_score = int(file.read())
score_font = pygame.font.Font(None, 50)
high_score_text = score_font.render(f'High: {player_high_score}', 1, "black")
current_score_text = score_font.render(f'Score: {player_cur_score}', 1, "black")
score_text = None
level_x = None
level_y = None
is_alive = True
camera = Camera()

menu_buttons = []
obstacles_sprites = pygame.sprite.Group()
environment_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
ground_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


TILE_WIDHT = TILE_HEIGHT = 50 #размер одной клетки

tile_images = { #картинки спрайтов
    'wall': pygame.transform.scale(load_image('pictures\\box.png'), (TILE_WIDHT, TILE_HEIGHT)),
    'tree': pygame.transform.scale(load_image('pictures\\tree.png'), (TILE_WIDHT, TILE_HEIGHT)),
    'land': pygame.transform.scale(load_image('pictures\\land.png'), (TILE_WIDHT, TILE_HEIGHT))
}

#картинки
player_image = pygame.transform.scale(load_image('pictures\\mar.png'), (TILE_WIDHT * 2, TILE_HEIGHT))
ground_image = pygame.transform.scale(load_image('pictures\\ground.png'), (WIDTH, TILE_HEIGHT * KOEF))
background_image = pygame.transform.scale(load_image('pictures\\background.png'), (WIDTH, HEIGHT))
fon = pygame.transform.scale(load_image('pictures\\fon.jpg'), (WIDTH, HEIGHT))
retry_btn_image = pygame.transform.scale(load_image('pictures\\retry.png'), (90, 90))
quit_btn_image = pygame.transform.scale(load_image('pictures\\quit.png'), (75, 75))

Start_screen()
fly_timer = pygame.USEREVENT + 1  # таймер для полёта птицы
score_timer = pygame.USEREVENT + 2  # таймер, по которому начисляется время
pygame.time.set_timer(fly_timer, 3)
pygame.time.set_timer(score_timer, 3000)
T = 0
pygame.key.set_repeat(10, 10)
while True:
    for event in pygame.event.get():
        if event.type == fly_timer and player:
            player.rect = player.rect.move(1, 0)
        if event.type == score_timer and player:
            player_cur_score += 1
            current_score_text = score_font.render(f'Score: {player_cur_score}', 1, "black")
            if player_cur_score > player_high_score:
                player_high_score += 1
                high_score_text = score_font.render(f'High: {player_high_score}', 1, "black")
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            terminate()
        if player and event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
           player.rect = player.rect.move(0, -10)
        if player and event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
           player.rect = player.rect.move(0, 10)
    if player:
        screen.fill((0, 0, 0))
        screen.blit(background_image, (T, 0))
        screen.blit(background_image, (T + WIDTH, 0))
        if T < -WIDTH:
            T = 0
        T -= 1
        camera.update(player)
        for sprite in all_sprites:
            if pygame.sprite.collide_mask(player, sprite) and (sprite in obstacles_sprites or sprite in ground_sprites):
                is_alive = False
            camera.apply(sprite)
    else:
        for btn in menu_buttons:
            btn.process()
    all_sprites.draw(screen)
    player_sprite.draw(screen)
    if player:
        screen.blit(high_score_text, (WIDTH - high_score_text.get_width() * 1.5, high_score_text.get_height()))
        screen.blit(current_score_text, (WIDTH - high_score_text.get_width() * 1.5, high_score_text.get_height() * 2))
    else:
        screen.blit(high_score_text, (WIDTH - high_score_text.get_width() * 1.5, high_score_text.get_height()))
    pygame.display.flip()
    if not is_alive:
        Lose_screen(LOSESCREEN_WIDHT, LOSESCREEN_HEIGHT)
