# This is a sample Python script.
import random
import sys
from time import sleep

import pygame
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

pygame.init()

clock = pygame.time.Clock()
FPS = 60

pixels = 1000  # How wide the window will be
screen_height = pixels  # how high the window will be
screen_width = screen_height
screen = pygame.display.set_mode((screen_width, screen_height))  # creates the screen


grid_size = 50
rect_size = pixels/grid_size
grid = []
for x in range(grid_size):
    tmp = []
    for y in range(grid_size):
        if x == 0 or x == grid_size-1:
            tmp.append(10)
            continue
        elif y == 0 or y == grid_size-1:
            tmp.append(9)
            continue
        tmp.append(-1)
    grid.append(tmp)

grid[0][0] = 5
grid[0][grid_size-1] = 7
grid[grid_size-1][0] = 6
grid[grid_size-1][grid_size-1] = 8


up_img = pygame.transform.scale(pygame.image.load('up.png'), (rect_size, rect_size))
down_img = pygame.transform.scale(pygame.image.load('down.png'), (rect_size, rect_size))
left_img = pygame.transform.scale(pygame.image.load('left.png'), (rect_size, rect_size))
right_img = pygame.transform.scale(pygame.image.load('right.png'), (rect_size, rect_size))
clear_img = pygame.transform.scale(pygame.image.load('clear.png'), (rect_size, rect_size))
up_left_img = pygame.transform.scale(pygame.image.load('up-left.png'), (rect_size, rect_size))
up_right_img = pygame.transform.scale(pygame.image.load('up-right.png'), (rect_size, rect_size))
down_left_img = pygame.transform.scale(pygame.image.load('down-left.png'), (rect_size, rect_size))
down_right_img = pygame.transform.scale(pygame.image.load('down-right.png'), (rect_size, rect_size))
horizontal_img = pygame.transform.scale(pygame.image.load('horizontal.png'), (rect_size, rect_size))
vertical_img = pygame.transform.scale(pygame.image.load('vertical.png'), (rect_size, rect_size))
direction_image_enum = {0: clear_img, 1:up_img, 2:right_img, 3:down_img, 4:left_img,
                        5:up_left_img, 6:up_right_img, 7:down_left_img, 8:down_right_img,
                        9:horizontal_img, 10:vertical_img}


def draw():
    for x in range(grid_size):
        for y in range(grid_size):
            if grid[x][y] == -1:
                pygame.draw.rect(screen, (0, 0, 0),
                    pygame.Rect(x*rect_size, y*rect_size, rect_size, rect_size))
            else:
                screen.blit(direction_image_enum[grid[x][y]], (x*rect_size, y*rect_size),
                    pygame.Rect(0, 0, rect_size, rect_size))

    pygame.display.flip()


def remove_options(options, to_remove_arr):
    if options is None or to_remove_arr is None:
        return options
    for to_remove in to_remove_arr:
        if to_remove in options:
            options.remove(to_remove)
    return options


def rem_left(options, left_tile):
    # left_tile etwas nach rechts
    if left_tile == 1 or left_tile == 2 or left_tile == 3 or left_tile == 5 or left_tile == 7 or left_tile == 9:
        # alles weg was nichts nach links hat
        options = remove_options(options, [0, 2, 5, 7, 10])
    # left_tile nichts nach rechts
    if left_tile == 0 or left_tile == 4 or left_tile == 6 or left_tile == 8 or left_tile == 10:
        options = remove_options(options, [1, 3, 4, 6, 8, 9])
    return options


def rem_right(options, right_tile):
    # right_tile etwas nach links
    if right_tile == 1 or right_tile == 3 or right_tile == 4 or right_tile == 6 or right_tile == 8 or right_tile == 9:
        # alles weg was nichts nach rechts hat
        options = remove_options(options, [0, 4, 6, 8, 10])
    # right_tile nichts nach links
    if right_tile == 0 or right_tile == 2 or right_tile == 5 or right_tile == 7 or right_tile == 10:
        # alles weg was etwas nach rechts hat
        options = remove_options(options, [1, 2, 3, 5, 7, 9])
    return options


def rem_up(options, up_tile):
    # up_tile nichts nach unten
    if up_tile == 0 or up_tile == 1 or up_tile == 7 or up_tile == 8 or up_tile == 9:
        # remove alles was etwas nach oben hat
        options = remove_options(options, [1, 2, 4, 7, 8, 10])
    # up_tile etwas nach unten
    if up_tile == 2 or up_tile == 3 or up_tile == 4 or up_tile == 5 or up_tile == 6 or up_tile == 10:
        # remove alles was nichts nach oben hat
        options = remove_options(options, [0, 3, 5, 6, 9])
    return options


def rem_down(options, down_tile):
    # down_tile nichts nach oben
    if down_tile == 0 or down_tile == 3 or down_tile == 5 or down_tile == 6 or down_tile == 9:
        # remove alles was etwas nach unten hat
        options = remove_options(options, [2, 3, 4, 5, 6, 10])
    # down_tile etwas nach oben
    if down_tile == 1 or down_tile == 2 or down_tile == 4 or down_tile == 7 or down_tile == 8 or down_tile == 10:
        # remove alles was nichts nach unten hat
        options = remove_options(options, [0, 1, 7, 8, 9])
    return options


def define_entropy_for_tile(x, y):
    tile = grid[x][y]
    if tile != -1:
        return []
    left_tile = grid[x-1][y]
    right_tile = grid[x+1][y]
    up_tile = grid[x][y-1]
    down_tile = grid[x][y+1]
    options = [*direction_image_enum]

    if left_tile != -1:
        options = rem_left(options, left_tile)
    if right_tile != -1:
        options = rem_right(options, right_tile)
    if up_tile != -1:
        options = rem_up(options, up_tile)
    if down_tile != -1:
        options = rem_down(options, down_tile)
    return options


def step():
    entropy = []
    for x in range(grid_size-1):
        tmp = []
        for y in range(grid_size-1):
            if x == 0 or x == grid_size-1 or y == 0 or y == grid_size-1:
                continue
            tmp.append((y, define_entropy_for_tile(x, y)))
        entropy.append((x, tmp))


    lowest_entropy_candidates = []
    lowest_seen_entropy = 100
    for x, entropy_x in entropy:
        for y, single_entropy in entropy_x:
            if single_entropy is None:
                continue
            if len(single_entropy) == 0 or len(single_entropy) > lowest_seen_entropy:
                continue
            if len(single_entropy) == lowest_seen_entropy:
                lowest_entropy_candidates.append((x, y, single_entropy))
                continue
            if len(single_entropy) < lowest_seen_entropy:
                lowest_entropy_candidates = [(x, y, single_entropy)]
                lowest_seen_entropy = len(single_entropy)


    # collapse one of lowest
    if len(lowest_entropy_candidates) == 0: return
    to_collapse = lowest_entropy_candidates[random.randint(0, len(lowest_entropy_candidates)-1)]
    options = to_collapse[2]
    grid[to_collapse[0]][to_collapse[1]] = options[random.randint(0, len(to_collapse[2])-1)]


def loop():
    global FPS
    while True:
        draw()
        # sleep(1)
        clock.tick(FPS)
        step()
        for event in pygame.event.get():  # Allows you to add various events
            if event.type == pygame.QUIT:  # Allows the user to exit using the X button
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

loop()