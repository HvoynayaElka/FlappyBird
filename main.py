import os
import sys

import pygame

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Flappy bird")

bg = pygame.image.load('images/bg.png')
birds_fly = [pygame.image.load('images/bird/bird_2_1.png'), 
             pygame.image.load('images/bird/bird_2_2.png'),
             pygame.image.load('images/bird/bird_2_3.png'),
             pygame.image.load('images/bird/bird_2_4.png'),
             pygame.image.load('images/bird/bird_2_5.png'),
             pygame.image.load('images/bird/bird_2_6.png'),
             pygame.image.load('images/bird/bird_2_7.png'),
             pygame.image.load('images/bird/bird_2_8.png'),
             pygame.image.load('images/bird/bird_2_9.png'),
             pygame.image.load('images/bird/bird_2_10.png'),
             pygame.image.load('images/bird/bird_2_11.png'),
             pygame.image.load('images/bird/bird_2_12.png'),
             pygame.image.load('images/bird/bird_2_13.png'),
             pygame.image.load('images/bird/bird_2_14.png')]
player_anim_count = 0

bg_x = 0

player_speed = 50
player_y = 500

bg_sound = pygame.mixer.Sound('sounds/les.mp3')
bg_sound.play()

running = True
while running:
    player = birds_fly[player_anim_count]
    colorkey = -1
    colorkey = player.get_at((0, 0))
    player.set_colorkey(colorkey)
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1920, 0))
    screen.blit(player, (300, player_y))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and player_y > 50:
        player_y -= player_speed
    elif player_y < 800:
        player_y += player_speed / 5

    if player_anim_count == 13:
        player_anim_count = 0
    else:
        player_anim_count += 1

    bg_x -= 2
    if bg_x == -1920:
        bg_x = 0

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    clock.tick(20)
