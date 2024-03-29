import pygame
import sys
from Funcs import load_image, load_level, levels_count


class Start_screen:
    def __init__(self):
        self.koef_coord = 0.5
        self.delta_coord = 100
        self.main_menu()

    def main_menu(self):
        screen.blit(fon, (0, 0))
        main_font = pygame.font.Font(None, 150)
        string_rendered = main_font.render('Flappy bird', 1, "#d1e231")
        screen.blit(string_rendered, (WIDTH / 5, HEIGHT / 6))
        text = ['Играть', 'Выбрать уровень', 'Выйти']
        btn_width, btn_height = 250, 50
        Button(WIDTH / 20, HEIGHT * self.koef_coord, btn_width, btn_height, menu_buttons, text[0], start_game)
        Button(WIDTH / 20, HEIGHT * self.koef_coord + self.delta_coord, btn_width, btn_height, menu_buttons, text[1],
               self.choose_level)
        Button(WIDTH / 20, HEIGHT * self.koef_coord + self.delta_coord * 2, btn_width,
               btn_height, menu_buttons, text[2], terminate)

    def choose_level(self):
        all_levels = levels_count()
        menu_buttons.clear()
        screen.blit(fon, (0, 0))
        Button(WIDTH / 2, HEIGHT * self.koef_coord + self.delta_coord * 0, 300, 50,
               menu_buttons, f'Уровень {all_levels[0][:-4]}', lambda: start_game(all_levels[0]))
        Button(WIDTH / 2, HEIGHT * self.koef_coord + self.delta_coord * 1, 300, 50,
               menu_buttons, f'Уровень {all_levels[1][:-4]}', lambda: start_game(all_levels[1]))
        Button(WIDTH / 2, HEIGHT * self.koef_coord + self.delta_coord * 2, 300, 50,
               menu_buttons, f'Уровень {all_levels[2][:-4]}', lambda: start_game(all_levels[2]))


class Lose_screen:
    def __init__(self, width, height, text, text_color):
        self.width = width
        self.height = height
        self.check = True
        self.text = text
        self.text_color = text_color
        self.Surf = pygame.Surface((self.width, self.height))
        self.main_font = pygame.font.Font(None, 75)
        self.string_rendered = self.main_font.render(self.text, 1, self.text_color)
        self.button_list = []
        self.Retry_btn = Button((WIDTH - self.width) * 1.2, (HEIGHT - self.height) * 1.1,
                                retry_btn_image_normal.get_width(),
                                retry_btn_image_normal.get_height(), self.button_list,
                                onclickFunction=self.restart_game, image_normal=retry_btn_image_normal,
                                image_hover=retry_btn_image_hover)
        self.Quit_btn = Button((WIDTH - self.width) * 0.6, (HEIGHT - self.height) * 1.1,
                               quit_btn_image_normal.get_width(), quit_btn_image_normal.get_width(), self.button_list,
                               onclickFunction=self.go_to_menu, image_normal=quit_btn_image_normal,
                               image_hover=quit_btn_image_hover)
        self.update()

    def restart_game(self):
        self.destroy()
        start_game(level_name)

    def destroy(self):
        global player, level_x, level_y, is_alive, is_win, player_speed_x,\
            player_speed_y, obstacles_sprites, \
            environment_sprites, player_sprite, ground_sprites,\
            all_sprites, player_cur_score, current_score_text
        obstacles_sprites = pygame.sprite.Group()
        environment_sprites = pygame.sprite.Group()
        player_sprite = pygame.sprite.Group()
        ground_sprites = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        player, level_x, level_y, is_alive, is_win = None, None, None, True, False
        player_speed_y = 1
        player_speed_x = 1
        self.check = False
        self.button_list.clear()
        player_cur_score = 0
        current_score_text = score_font.render(f'Score: {player_cur_score}', 1, "black")

    def update(self):
        self.Surf.blit(lose_screen_image, (0, 0))
        self.Surf.blit(self.string_rendered,
                       ((self.Surf.get_width() - self.string_rendered.get_width()) / 2,
                        (self.Surf.get_height() - self.string_rendered.get_height()) / 4))
        while self.check:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                    terminate()
            screen.blit(self.Surf, ((WIDTH - self.width) / 2, (HEIGHT - self.height) / 2))
            for button in self.button_list:
                button.process()
            pygame.display.flip()

    def go_to_menu(self):
        self.destroy()
        Start_screen()


class Victory_screen(Lose_screen):
    def __init__(self, width, height, text, text_color):
        self.width = width
        self.height = height
        self.check = True
        self.text = text
        self.text_color = text_color
        self.file_number = int(level_name[0])
        self.Surf = pygame.Surface((self.width, self.height))
        self.main_font = pygame.font.Font(None, 75)
        self.string_rendered = self.main_font.render(self.text, 1, self.text_color)
        self.button_list = []
        self.Retry_btn = Button((WIDTH - self.width) * 1.2, (HEIGHT - self.height) * 1.1,
                                retry_btn_image_normal.get_width(),
                                retry_btn_image_normal.get_height(), self.button_list,
                                onclickFunction=self.restart_game, image_normal=retry_btn_image_normal,
                                image_hover=retry_btn_image_hover)
        self.Quit_btn = Button((WIDTH - self.width) * 0.6, (HEIGHT - self.height) * 1.1,
                               quit_btn_image_normal.get_width(), quit_btn_image_normal.get_width(), self.button_list,
                               onclickFunction=terminate, image_normal=quit_btn_image_normal,
                               image_hover=quit_btn_image_hover)
        self.next_btn = Button((WIDTH - self.width) * 0.9, (HEIGHT - self.height) * 1.1,
                               next_btn_image_normal.get_width(),
                               next_btn_image_normal.get_height(), self.button_list,
                               onclickFunction=self.next_level, image_normal=next_btn_image_normal,
                               image_hover=next_btn_image_hover)
        self.update()

    def next_level(self):
        global player, level_x, level_y, is_alive, is_win, obstacles_sprites, \
            environment_sprites, player_sprite, ground_sprites,\
            all_sprites, player_cur_score, current_score_text
        obstacles_sprites = pygame.sprite.Group()
        environment_sprites = pygame.sprite.Group()
        player_sprite = pygame.sprite.Group()
        ground_sprites = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        player, level_x, level_y, is_alive, is_win = None, None, None, True, False
        self.file_number += 1
        self.check = False
        player_cur_score = 0
        current_score_text = score_font.render(f'Score: {player_cur_score}', 1, "black")
        if self.file_number > len(levels_count()):
            self.file_number = 1
        start_game(str(self.file_number) + '.txt')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        global finish_sprite
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        if tile_type == 'tree':
            environment_sprites.add(self)
            self.rect = self.image.get_rect().move(TILE_WIDHT * pos_x, TILE_HEIGHT * pos_y)
        elif tile_type == 'finish':
            finish_sprite = self
            self.rect = self.image.get_rect().move(TILE_WIDHT * pos_x, TILE_HEIGHT * pos_y)
        elif tile_type == 'obs_end':
            obstacles_sprites.add(self)
            self.rect = self.image.get_rect().move(TILE_WIDHT * pos_x - 5, TILE_HEIGHT * pos_y) # вычитается 5 пикселей, для того, чтобы верхушка трубы примерно ровно встала, трудно просчитать, какой должен быть коэфф.
        else:
            obstacles_sprites.add(self)
            self.rect = self.image.get_rect().move(TILE_WIDHT * pos_x, TILE_HEIGHT * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_sprite, all_sprites)
        self.frames = player_images
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(TILE_WIDHT * pos_x, TILE_HEIGHT * pos_y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Camera:
    def __init__(self):
        self.dx = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        if is_endless_level:
            if obj in ground_sprites and obj.rect.x <= -WIDTH:
                obj.rect.x += WIDTH * 2
            elif obj in obstacles_sprites and obj.rect.x <= -TILE_WIDHT * 2:
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
            self.rect = self.image.get_rect().move(WIDTH * k, -TILE_HEIGHT * 2 * KOEF)


class Button:
    def __init__(self, x, y, width, height, btn_group, button_text='Button',
                 onclickFunction=None, image_normal=None,
                 image_hover=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.btn_group = btn_group
        self.btn_image = None
        self.onclickFunction = onclickFunction
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        if image_normal is None:
            self.button_text = button_text
            self.fillColors = {'normal': (20, 20, 20), 'hover': '#ffff66'}
            self.main_font = pygame.font.Font(None, 50)
            self.display_text = self.main_font.render(button_text, True, (20, 20, 20))
        else:
            self.btn_image = {'normal': image_normal, 'hover': image_hover}
        self.btn_group.append(self)

    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.btn_image is None:
            self.display_text = self.main_font.render(self.button_text, True, self.fillColors["normal"])
            if self.buttonRect.collidepoint(mouse_pos):
                self.display_text = self.main_font.render(self.button_text, True, self.fillColors["hover"])
                if pygame.mouse.get_pressed()[0]:
                    self.onclickFunction()
            if self in menu_buttons:
                screen.blit(self.display_text, self.buttonRect)
        else:
            self.image = self.btn_image['normal']
            if self.buttonRect.collidepoint(mouse_pos):
                self.image = self.btn_image['hover']
                if pygame.mouse.get_pressed()[0]:
                    self.onclickFunction()
            if self in self.btn_group:
                screen.blit(self.image, self.buttonRect)


def start_game(filename=None):
    global player,\
        level_x, level_y, score_text, \
        is_endless_level, level_name
    menu_buttons.clear()
    bg_sound.play()
    if not filename:
        is_endless_level = True
        player, level_x, level_y = generate_level(load_level('levels\\main_map.txt'))
    else:
        is_endless_level = False
        level_name = filename
        player, level_x, level_y = generate_level(load_level(f'levels\\other levels\\{filename}'))
    if not is_endless_level:
        for i in range(4):
            Ground(i)
            Ground(i, upper=True)
    else:
        Ground(0)
        Ground(1)
        Ground(0, upper=True)
        Ground(1, upper=True)


def generate_level(level):  # генерация уровня из файла
    new_player = None
    x = None
    y = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('vert_wall', x, y)
            elif level[y][x] == '_':
                Tile('gor_wall', x, y)
            elif level[y][x] == '&':
                Tile('obs_end', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == '!':
                Tile('tree', x, y)
            elif level[y][x] == '-':
                Tile('land', x, y)
            elif level[y][x] == '|':
                Tile('finish', x, y)

    return new_player, x, y


def terminate():
    pygame.quit()
    with open('data\\player result\\info.txt', 'w') as file:
        file.write(str(player_high_score))
    sys.exit()


pygame.init()
# различные константы
WIDTH = 960
HEIGHT = 540
KOEF = 1.4
player_speed_y = 1
vy = 2
delta_vy = 5
player_speed_x = 1
LOSESCREEN_WIDHT = WIDTH / 2
LOSESCREEN_HEIGHT = HEIGHT / 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))

player = None
player_cur_score = 0
with open('data\\player result\\info.txt') as file:  # чтение рекорда очков из файла
    player_high_score = int(file.read())
score_font = pygame.font.Font(None, 50)
high_score_text = score_font.render(f'High: {player_high_score}', 1, "black")
current_score_text = score_font.render(f'Score: {player_cur_score}', 1, "black")
score_text = None
level_name = None
level_x = None
level_y = None
is_alive = True  # меняется при столкновении
is_win = False  # меняется, когда доходим до финиша
is_endless_level = True  # если True, то уровень подобен кольцу, финиша нет.
camera = Camera()

menu_buttons = []
obstacles_sprites = pygame.sprite.Group()
environment_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
ground_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
finish_sprite = None  # Спрайт финиша (нет в бесконченом уровне)

TILE_WIDHT = TILE_HEIGHT = 50  # размер одной клетки
BIRD_WIDTH, BIRD_HEIGHT = 40, 40

tile_images = {  # картинки спрайтов
    'vert_wall': pygame.transform.scale(load_image('pictures\\vert_box.png'), (TILE_WIDHT, TILE_HEIGHT)),
    'tree': pygame.transform.scale(load_image('pictures\\tree.png'), (TILE_WIDHT, TILE_HEIGHT)),
    'land': pygame.transform.scale(load_image('pictures\\land.png'), (TILE_WIDHT, TILE_HEIGHT)),
    'finish': load_image('pictures\\finish.png'),
    'obs_end': pygame.transform.scale(load_image('pictures\\box_end.png'), (TILE_WIDHT * 1.2, TILE_HEIGHT)),
    'gor_wall': pygame.transform.scale(load_image('pictures\\gor_box.png'), (TILE_WIDHT, TILE_HEIGHT)),
}

# картинки
player_images = [pygame.transform.scale(load_image('pictures/bird/bird_2_1.png', -1), (BIRD_WIDTH, BIRD_HEIGHT)),
                 pygame.transform.scale(load_image('pictures/bird/bird_2_2.png', -1), (BIRD_WIDTH, BIRD_HEIGHT)),
                 pygame.transform.scale(load_image('pictures/bird/bird_2_3.png', -1), (BIRD_WIDTH, BIRD_HEIGHT)),
                 pygame.transform.scale(load_image('pictures/bird/bird_2_4.png', -1), (BIRD_WIDTH, BIRD_HEIGHT)),
                 pygame.transform.scale(load_image('pictures/bird/bird_2_5.png', -1), (BIRD_WIDTH, BIRD_HEIGHT)),
                 pygame.transform.scale(load_image('pictures/bird/bird_2_6.png', -1), (BIRD_WIDTH, BIRD_HEIGHT)),
                 pygame.transform.scale(load_image('pictures/bird/bird_2_7.png', -1), (BIRD_WIDTH, BIRD_HEIGHT)),
                 pygame.transform.scale(load_image('pictures/bird/bird_2_8.png', -1), (BIRD_WIDTH, BIRD_HEIGHT)),
                 pygame.transform.scale(load_image('pictures/bird/bird_2_9.png', -1), (BIRD_WIDTH, BIRD_HEIGHT)),
                 pygame.transform.scale(load_image('pictures/bird/bird_2_10.png', -1), (BIRD_WIDTH, BIRD_HEIGHT)),
                 pygame.transform.scale(load_image('pictures/bird/bird_2_11.png', -1), (BIRD_WIDTH, BIRD_HEIGHT)),
                 pygame.transform.scale(load_image('pictures/bird/bird_2_12.png', -1), (BIRD_WIDTH, BIRD_HEIGHT)),
                 pygame.transform.scale(load_image('pictures/bird/bird_2_13.png', -1), (BIRD_WIDTH, BIRD_HEIGHT)),
                 pygame.transform.scale(load_image('pictures/bird/bird_2_14.png', -1), (BIRD_WIDTH, BIRD_HEIGHT))]
ground_image = pygame.transform.scale(load_image('pictures\\ground.png'), (WIDTH, TILE_HEIGHT * KOEF))
background_image = pygame.transform.scale(load_image('pictures\\background.png'), (WIDTH, HEIGHT))
fon = pygame.transform.scale(load_image('pictures\\fon.png'), (WIDTH, HEIGHT))
retry_btn_image_normal = pygame.transform.scale(load_image('pictures\\retry_normal.png'), (90, 90))
retry_btn_image_hover = pygame.transform.scale(load_image('pictures\\retry_hover.png'), (90, 90))
quit_btn_image_normal = pygame.transform.scale(load_image('pictures\\quit_normal.png'), (90, 90))
quit_btn_image_hover = pygame.transform.scale(load_image('pictures\\quit_hover.png'), (90, 90))
next_btn_image_normal = pygame.transform.scale(load_image('pictures\\next_normal.png'), (90, 90))
next_btn_image_hover = pygame.transform.scale(load_image('pictures\\next_hover.png'), (90, 90))
lose_screen_image = pygame.transform.scale(load_image('pictures\\bg.jpg'), (LOSESCREEN_WIDHT, LOSESCREEN_HEIGHT))

Start_screen()
clock_vy = pygame.time.Clock()  # сила тяжести, действующая на птицу
bird_animation_timer = pygame.USEREVENT + 3  # таймер для анимации птицы
score_timer = pygame.USEREVENT + 2  # таймер, по которому начисляются очки
pygame.time.set_timer(score_timer, 4000)
pygame.time.set_timer(bird_animation_timer, 100)
T = 0  # T - период движения заднего фона
bg_sound = pygame.mixer.Sound('data\\sounds\\les.mp3')
bg_sound.set_volume(0.2)
while True:
    for event in pygame.event.get():
        if event.type == bird_animation_timer and player:
            player.update()
        if event.type == score_timer and player:
            player_cur_score += 1
            current_score_text = score_font.render(f'Score: {player_cur_score}', 1, "black")
            if player_cur_score > player_high_score:
                player_high_score += 1
                high_score_text = score_font.render(f'High: {player_high_score}', 1, "black")
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            terminate()
        if player and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player.rect.y > TILE_WIDHT:
            player_speed_y = -delta_vy
    if player:
        player.rect = player.rect.move(player_speed_x, 0)
        player.rect = player.rect.move(0, player_speed_y)
        if player_speed_y < vy:
            player_speed_y += vy / clock_vy.tick(120)
        screen.fill((0, 0, 0))
        screen.blit(background_image, (T, 0))
        screen.blit(background_image, (T + WIDTH, 0))
        if T < -WIDTH:
            T = 0
        T -= 1
        camera.update(player)
        for sprite in all_sprites:
            if finish_sprite and pygame.sprite.collide_mask(player, finish_sprite):
                is_win = True
            elif pygame.sprite.collide_mask(player, sprite) and (
                    sprite in obstacles_sprites or sprite in ground_sprites):
                is_alive = False
            camera.apply(sprite)
    else:
        for btn in menu_buttons:
            btn.process()
    all_sprites.draw(screen)
    player_sprite.draw(screen)
    if player and is_endless_level:  # заполняется после спрайтов для того, чтобы быть поверх всего остального
        screen.blit(high_score_text, (WIDTH - high_score_text.get_width() * 1.5,
                                      high_score_text.get_height()))  # коэффициенты подобраны без различных зависимостей
        screen.blit(current_score_text, (WIDTH - high_score_text.get_width() * 1.5,
                                         high_score_text.get_height() * 2))  # коэффициенты подобраны без различных зависимостей
    else:
        screen.blit(high_score_text, (WIDTH - high_score_text.get_width() * 1.5,
                                      high_score_text.get_height()))  # коэффициенты подобраны без различных зависимостей
    pygame.display.flip()
    if is_win:
        Victory_screen(LOSESCREEN_WIDHT, LOSESCREEN_HEIGHT, 'you win!', '#ffff66')
    elif not is_alive:
        bg_sound.stop()
        Lose_screen(LOSESCREEN_WIDHT, LOSESCREEN_HEIGHT, 'you lose', '#ff4d00')
